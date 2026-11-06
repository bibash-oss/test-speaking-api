"""
Downloads the Kokoro text-to-speech model and prepares it for the examiner's lip sync.

    python scripts/setup_kokoro.py            (needs the `onnx` package, see below)

Writes to models/:
    kokoro-v1.0-timed.onnx   the model, with one extra output called "duration"
    voices-v1.0.bin          the voice styles (bm_george, bm_fable, ...)

Why the patch: Kokoro works out how long every sound lasts before it makes any audio, but the
published model throws that information away. The avatar needs it to move the mouth with the
speech, so a single Identity node is added that exposes it as an output named "duration"
(kokoro-onnx looks for exactly that name). The audio is not changed in any way.
"""
import os
import sys
import tempfile
import urllib.request

RELEASE = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
MODELS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
MODEL_OUT = os.path.join(MODELS, "kokoro-v1.0-timed.onnx")
VOICES_OUT = os.path.join(MODELS, "voices-v1.0.bin")

# Where the model computes each sound's length (rounded, at least one frame). One frame is 600
# audio samples, i.e. 25 ms at the model's 24 kHz.
DURATION_NODE = "/encoder/Clip"


def download(name, destination):
    print(f"downloading {name} ...")
    with urllib.request.urlopen(RELEASE + name) as response, open(destination, "wb") as out:
        while chunk := response.read(1 << 20):
            out.write(chunk)


def patch(source, destination):
    try:
        import onnx
        from onnx import TensorProto, helper
    except ImportError:
        sys.exit("The `onnx` package is needed for this one-off step - install onnx to run setup.")

    model = onnx.load(source)
    node = next((n for n in model.graph.node if n.name == DURATION_NODE and n.op_type == "Clip"), None)
    if node is None:
        sys.exit(f"Could not find {DURATION_NODE} in the model; this is not the model version the patch was written for.")
    if any(o.name == "duration" for o in model.graph.output):
        sys.exit("The model already has a duration output.")

    model.graph.node.append(helper.make_node("Identity", [node.output[0]], ["duration"], name="/timing/duration"))
    model.graph.output.append(helper.make_tensor_value_info("duration", TensorProto.FLOAT, None))
    onnx.save(model, destination)
    print(f"wrote {destination}")


def main():
    force = "--force" in sys.argv
    os.makedirs(MODELS, exist_ok=True)

    if force or not os.path.exists(VOICES_OUT):
        download("voices-v1.0.bin", VOICES_OUT)
    if force or not os.path.exists(MODEL_OUT):
        with tempfile.TemporaryDirectory() as tmp:
            raw = os.path.join(tmp, "kokoro-v1.0.onnx")
            download("kokoro-v1.0.onnx", raw)
            patch(raw, MODEL_OUT)
    print("Kokoro is ready.")


if __name__ == "__main__":
    main()
