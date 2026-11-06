# Interview Voice AI API

Minimal Flask and Socket.IO interview MVP powered by:
- **AI Model**: Google Gemini (`gemini-2.5-flash`) for interview reasoning, conversational question flow, and candidate speech audio transcription.
- **Voice Model**: Kokoro TTS (`bm_george` voice, `kokoro-v1.0-timed.onnx` with phoneme lip-sync alignment).

---

## Architecture & Flow

```
   Candidate Speech (Audio / Text)
                │
                ▼
      ┌──────────────────┐
      │  Gemini 2.5 Flash│  ◄── Transcribes audio & reasons on interview context
      └─────────┬────────┘
                │
                ▼ Next Interviewer Question
      ┌──────────────────┐
      │    Kokoro TTS    │  ◄── Synthesizes realistic British male speech
      └─────────┬────────┘
                │
                ▼
     Base64 Audio + Lip-sync Phonemes + Next Question Text
```

---

## Quickstart

### 1. Activate Environment
```bash
source venv/bin/activate
```

### 2. Environment Variables (.env)
```env
PORT=5002
FLASK_DEBUG=True
SECRET_KEY=interview-voice-api-secret-key
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Run Server
```bash
python app.py
```

---

## API Endpoints

### 1. Health Check
- **GET** `/`
- **Response**:
  ```json
  {
    "status": "ok",
    "service": "interview-api",
    "ai_model": "gemini-2.5-flash",
    "voice_model": "kokoro-v1.0-timed (bm_george)"
  }
  ```

### 2. Company / Admin Job Management
- **POST** `/api/jobs`: Create job position with Title, Level, Description, and Company Name.
  ```json
  {
    "title": "Backend Engineer",
    "level": "Senior",
    "description": "Building microservices with Python, PostgreSQL, and Kafka.",
    "company_name": "Ktmbees"
  }
  ```
  Returns the created job and public `invite_url` (e.g. `http://localhost:3000/invite/<invite_token>`).
- **GET** `/api/jobs`: List all jobs and candidate applicant counts.
- **GET** `/api/jobs/<job_id>/candidates`: Candidate leaderboard with scores, recommendations, and status.
- **GET** `/api/candidates/<candidate_id>`: Detailed candidate report card, parsed resume, and full interview transcript.

### 3. Candidate Invitation & Registration
- **GET** `/api/invite/<token>`: Fetch job details for the candidate's welcome screen.
- **POST** `/api/invite/<token>/register`: Candidate registration (Name, Email, Phone, and PDF Resume upload).
  - Automatically parses PDF resume via Gemini.
  - Generates a unique `session_token` for the interview session.

### 4. Start Interview
- **POST** `/api/interview/start`
- **Body**:
  ```json
  {
    "session_id": "<session_token>",
    "role": "Backend Engineer",
    "level": "Senior"
  }
  ```
- **Response**:
  ```json
  {
    "session_id": "session_123",
    "stage": 1,
    "text": "Hello, John! Welcome to your interview today for the Senior Backend Engineer role at Ktmbees...",
    "audio": "<base64_wav>",
    "lipsync": [["h", 0, 80], ...],
    "is_complete": false
  }
  ```

### 5. Respond (Candidate Speech / Text)
- **POST** `/api/interview/respond`
- **JSON Request (Text or Base64 Audio)**:
  ```json
  {
    "session_id": "session_123",
    "audio": "<base64_audio_blob>",
    "mime_type": "audio/webm"
  }
  ```
  *or with direct text:*
  ```json
  {
    "session_id": "session_123",
    "text": "I have experience with Python and distributed systems."
  }
  ```
- **Multipart Form Upload**:
  You can also upload an audio file directly (`audio=@recording.webm`, with form fields `session_id`).
- **Response**:
  ```json
  {
    "session_id": "session_123",
    "candidate_text": "I have experience with Python and distributed systems.",
    "stage": 2,
    "text": "That's great! Could you elaborate on a challenging distributed system you designed?",
    "audio": "<base64_wav>",
    "lipsync": [...],
    "is_complete": false
  }
  ```

---

## Socket.IO Real-time Events

| Event Sent | Payload | Description |
| :--- | :--- | :--- |
| `join` | `{"session_id": "123"}` | Joins a room for real-time messages. |
| `start_interview` | `{"session_id": "123", "role": "Backend Engineer"}` | Triggers greeting question and voice. |
| `candidate_speech` | `{"session_id": "123", "audio": "<base64>", "mime_type": "audio/webm"}` | Transcribes speech with Gemini, responds, and synthesizes speech. |
| `speak` | `{"text": "Any custom text"}` | Standalone TTS synthesis. |

| Event Received | Payload | Description |
| :--- | :--- | :--- |
| `interviewer_message` | `{"text": "...", "audio": "<b64>", "lipsync": [...], "stage": 1}` | Interviewer's next question with audio. |
| `candidate_transcript`| `{"text": "Transcribed speech..."}` | Emits what Gemini transcribed from candidate speech. |
| `processing_status` | `{"status": "transcribing_audio" \| "generating_question"}` | Progress updates. |
