"""
The examiner's voice: Kokoro (82M parameters, Apache 2.0), a British male voice, run on the CPU.

Every spoken line is returned as a WAV together with lip-sync cues - [sound, start_ms, duration_ms] -
which the 3D examiner uses to shape its mouth. The cues come from the sound lengths the model itself
works out (see scripts/setup_kokoro.py, which adds that output to the published model).
"""
import base64
import collections
import io
import os
import re
import threading
import wave

import numpy as np

_MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_PATH = os.path.join(_MODELS, "kokoro-v1.0-timed.onnx")
VOICES_PATH = os.path.join(_MODELS, "voices-v1.0.bin")

# British male voices in the model: bm_george, bm_fable, bm_lewis, bm_daniel.
VOICE = "bm_george"
LANG = "en-gb"

# Speaking speed: 1.0 is the voice's natural pace, which is where Kokoro sounds its smoothest (slowing it
# down adds roughness). The calm delivery comes from the pauses below instead.
SPEED = 1.0

# Silence after a sentence's full stop / question mark, and after a comma (seconds). The model leaves
# only a short gap by itself, so it is topped up to these.
SENTENCE_PAUSE = 0.4
CLAUSE_PAUSE = 0.1

# Kokoro is unreliable on a very short input: "Thank you." on its own ends with a pitch dive of over an
# octave and lasts more than a second, which sounds eerie. Up to this many words, the phrase is rendered
# at the start of a longer sentence and cut off where it ends, which gives it normal intonation.
SHORT_PHRASE_WORDS = 4
_CARRIER = "Let's carry on with the next question."
FADE_S = 0.012  # fade-out where a short phrase is cut, so there is no click

# A sentence of at most this many words that is followed by more speech ("Thank you. Do you...") is joined
# to it with a comma, so it flows into it instead of stopping first.
JOIN_WORDS = 2

# Threads for the model. More is not faster: on a 10-core machine 4 was quicker than 10 and leaves room for
# other candidates at the same time.
MAX_THREADS = 4

# Finished lines are remembered, so a line that repeats (the fixed Part 2 instructions) is not re-rendered.
CACHE_SIZE = 64

# Every line is brought to the same loudness (average level of the speech, 0-1 of full scale).
TARGET_LEVEL = 0.16
MAX_GAIN = 2.5
MIN_GAIN = 0.4
PEAK_LIMIT = 0.92

LEAD_KEEP_S = 0.12   # silence left before the first word. Phones and Bluetooth speakers swallow the first
                     # 50-150 ms of audio while they wake up; it must be silence that they swallow.
FADE_IN_S = 0.01     # fade-in over the first word's first moment, so it never starts with a pop
# The model reads the first word of a line about 3 dB louder than the rest, so it jumps out. It is eased
# down by this much for the length of that word, then brought back over RELEASE_S.
FIRST_WORD_EASE_DB = 2.2
RELEASE_S = 0.12
TRAIL_KEEP_S = 0.06  # ... and after the last
_SILENCE_FRACTION = 0.03  # below 3% of the peak counts as silence

# Authors can request silence anywhere in a line with "[[pause:1000]]" (ms).
PAUSE_PATTERN = re.compile(r"\[\[pause:(\d+)\]\]")

_SPOKEN = [  # abbreviations read as words
    (re.compile(r"\bDr\.", re.I), "Doctor"), (re.compile(r"\bMr\."), "Mister"), (re.compile(r"\bMrs\."), "Missus"),
    (re.compile(r"\bMs\."), "Miss"), (re.compile(r"\bProf\.", re.I), "Professor"), (re.compile(r"\bvs\.", re.I), "versus"),
    (re.compile(r"\be\.g\.", re.I), "for example,"), (re.compile(r"\bi\.e\.", re.I), "that is,"),
    (re.compile(r"\betc\.", re.I), "et cetera"),
]

_kokoro = None
_kokoro_lock = threading.Lock()


def _get_kokoro():
    global _kokoro
    if _kokoro is None:
        with _kokoro_lock:
            if _kokoro is None:
                if not (os.path.exists(MODEL_PATH) and os.path.exists(VOICES_PATH)):
                    raise FileNotFoundError("The Kokoro voice files are missing - run: python scripts/setup_kokoro.py")
                import onnxruntime as ort
                from kokoro_onnx import Kokoro

                options = ort.SessionOptions()
                options.intra_op_num_threads = max(1, min(MAX_THREADS, os.cpu_count() or 1))
                session = ort.InferenceSession(MODEL_PATH, sess_options=options, providers=["CPUExecutionProvider"])
                _kokoro = Kokoro.from_session(session, VOICES_PATH)
    return _kokoro


_SENTENCES = re.compile(r"(?<=[.!?])\s+")


def _spoken(text):
    for pattern, words in _SPOKEN:
        text = pattern.sub(words, text)
    text = " ".join(text.split())
    # "Thank you. Do you..." -> "Thank you, do you...": a short opener flows into what follows.
    parts = _SENTENCES.split(text)
    for i in range(len(parts) - 1):
        if parts[i].endswith(".") and len(parts[i].split()) <= JOIN_WORDS:
            parts[i] = parts[i][:-1] + ","
    return " ".join(parts)


def _loud_edges(audio):
    """Index of the first and last sample that is clearly sound, or None for silence."""
    loud = np.nonzero(np.abs(audio) > max(1e-3, float(np.abs(audio).max()) * _SILENCE_FRACTION))[0]
    return (int(loud[0]), int(loud[-1])) if loud.size else None


def _ease_first_word(audio, rate, timings, onset):
    """Lowers the first word by FIRST_WORD_EASE_DB (in place), returning to full level after it."""
    word_end = next((e for p, s, e in timings if p in " .,?!;:" and s * rate > onset + 0.05 * rate), None)
    end = int(word_end * rate) if word_end else onset + int(0.3 * rate)
    release = int(RELEASE_S * rate)
    gain = np.ones(min(len(audio), end + release) - onset, dtype=np.float32)
    low = 10 ** (-FIRST_WORD_EASE_DB / 20)
    gain[: max(0, end - onset)] = low
    tail = gain[max(0, end - onset):]
    if tail.size:
        gain[max(0, end - onset):] = np.linspace(low, 1.0, tail.size, dtype=np.float32)
    audio[onset:onset + len(gain)] *= gain


def _render(text):
    """One stretch of speech as (audio float32, sample rate, [(sound, start s, end s)] or None)."""
    kokoro = _get_kokoro()
    spoken = _spoken(text)
    short = len(spoken.split()) <= SHORT_PHRASE_WORDS
    if short:
        if spoken[-1:] not in ".?!":
            spoken += "."
        spoken_in_context = f"{spoken} {_CARRIER}"
    else:
        spoken_in_context = spoken

    # A leading comma makes the model begin with a short silence and then rise into the first word. Without
    # it the audio starts at the first sound's full strength (up to half of peak volume on sample 0): a
    # click, and the first word feels cut in.
    audio, rate, timed = kokoro.create_timed(
        ", " + spoken_in_context, VOICE, SPEED, LANG,
        sentence_pause=SENTENCE_PAUSE, clause_pause=CLAUSE_PAUSE, continuous=kokoro.has_timings,
    )
    audio = np.asarray(audio, dtype=np.float32)
    timings = [(t.phoneme, float(t.start), float(t.end)) for t in timed] if timed else None

    if short and timings:
        # Keep only the phrase itself: up to the first full stop / question mark.
        end = next((i for i, t in enumerate(timings) if t[0] in ".?!"), None)
        if end is not None:
            cut = int(timings[end][2] * rate)
            timings = timings[: end + 1]
            audio = audio[:cut].copy()
            fade = min(len(audio), int(FADE_S * rate))
            if fade:
                audio[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)

    # The model pads its output with silence; trim to a small fixed amount, keeping the cues in step.
    edges = _loud_edges(audio)
    if edges:
        first = max(0, edges[0] - int(LEAD_KEEP_S * rate))
        last = min(len(audio), edges[1] + int(TRAIL_KEEP_S * rate))
        audio = audio[first:last]
        ramp = min(len(audio) - (edges[0] - first), int(FADE_IN_S * rate))
        if ramp > 0:
            start = edges[0] - first
            audio[start:start + ramp] *= np.linspace(0.0, 1.0, ramp, dtype=np.float32)
        if timings:
            shift = first / rate
            length = len(audio) / rate
            timings = [(p, max(0.0, s - shift), min(length, e - shift)) for p, s, e in timings if e - shift > 0 and s - shift < length]
            _ease_first_word(audio, rate, timings, edges[0] - first)
    return audio, rate, timings


def _level(audio):
    """Scales the line so its speech sits at TARGET_LEVEL, never clipping."""
    size = 480
    usable = len(audio) // size * size
    if usable == 0:
        return audio
    frames = np.sqrt(np.mean(audio[:usable].reshape(-1, size) ** 2, axis=1))
    loud = frames[frames > frames.max() * 0.15]
    if loud.size == 0 or loud.mean() < 1e-4:
        return audio
    gain = float(np.clip(TARGET_LEVEL / loud.mean(), MIN_GAIN, MAX_GAIN))
    peak = float(np.abs(audio).max())
    if peak * gain > PEAK_LIMIT:
        gain = PEAK_LIMIT / peak
    return audio * gain


def _cues(timings, total_ms):
    """Lip-sync cues covering the whole clip: gaps between sounds (pauses) are filled with silent cues."""
    cues, cursor = [], 0
    for phoneme, start, end in timings:
        start_ms, end_ms = round(start * 1000), round(end * 1000)
        if start_ms > cursor:
            cues.append(["." if start_ms - cursor > 120 else " ", cursor, start_ms - cursor])
        if end_ms > start_ms:
            cues.append([phoneme, start_ms, end_ms - start_ms])
        cursor = max(cursor, end_ms)
    if total_ms > cursor:
        cues.append([".", cursor, total_ms - cursor])
    return cues


def synthesize_speech(text):
    """Base64 WAV only - see synthesize_speech_with_lipsync."""
    return synthesize_speech_with_lipsync(text)[0]


_cache = collections.OrderedDict()
_cache_lock = threading.Lock()


def synthesize_speech_with_lipsync(text):
    """The rendered line, from memory when this exact line was spoken recently."""
    if not text:
        return None, None
    with _cache_lock:
        if text in _cache:
            _cache.move_to_end(text)
            return _cache[text]
    result = _synthesize(text)
    if result[0]:
        with _cache_lock:
            _cache[text] = result
            while len(_cache) > CACHE_SIZE:
                _cache.popitem(last=False)
    return result


def _synthesize(text):
    """
    Renders text to a base64 WAV in the examiner's voice.

    "[[pause:NNN]]" markers are replaced with NNN milliseconds of silence, so a line can be timed
    without splitting it into several clips (separate clips are how a voice seems to change).

    Returns (audio_b64, lipsync). lipsync is a list of [sound, start_ms, duration_ms] covering the WAV;
    it is None when the timings are unavailable, and the frontend then falls back to volume-driven
    lip sync.
    """
    if not text:
        return None, None

    try:
        pieces, rate, clock = [], None, 0.0
        cues_ok = True
        timings = []

        # re.split with a capturing group yields [text, ms, text, ms, text...], so odd indices are pauses.
        for index, segment in enumerate(PAUSE_PATTERN.split(text)):
            if index % 2 == 1:
                silence_for = int(segment) / 1000.0
                pieces.append(np.zeros(int((rate or 24000) * silence_for), dtype=np.float32))
                clock += silence_for
                continue
            if not segment.strip():
                continue

            audio, rate, spoken = _render(segment)
            if spoken is None:
                cues_ok = False
            elif cues_ok:
                timings += [(p, s + clock, e + clock) for p, s, e in spoken]
            pieces.append(audio)
            clock += len(audio) / rate

        if not pieces or not any(len(p) for p in pieces):
            return None, None

        audio = _level(np.concatenate(pieces))
        pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wav_file:
            wav_file.setframerate(rate)
            wav_file.setsampwidth(2)
            wav_file.setnchannels(1)
            wav_file.writeframes(pcm.tobytes())

        lipsync = _cues(timings, round(len(pcm) * 1000 / rate)) if cues_ok and timings else None
        return base64.b64encode(buffer.getvalue()).decode("utf-8"), lipsync

    except Exception as e:
        print(f"TTS Error: {e}")
        return None, None
