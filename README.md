# RepeatAfterMe.ai

**RepeatAfterMe.ai** is a full-stack web application that helps users improve their English pronunciation through LLMs. Whether you're a beginner or looking to sharpen your skills, this app offers a simple, engaging way to practice and learn how to pronounce words correctly.

---

## Features

- Presents words across multiple difficulty levels
- Records voice input directly in the browser
- Scores pronunciation with AI models
- Supports user account creation
- Saves words for future practice
- Tracks recent word history
- Easy deployment with Docker

---

## Prerequisites

- Docker Desktop
- PostgreSQL Connection URL (e.g., Supabase)
- Google Gemini API Key

---

## Running With Docker

Pull the official Docker image

```
docker pull repeatafterme1/repeatafterme
```

Run a Docker container

```
docker run -p 8000:8000 \
  -e DATABASE_URL="<your_postgres_connection_url>" \
  -e GEMINI_API_KEY="<your_google_gemini_key>" \
  repeatafterme1/repeatafterme
```

Once the container is running, open your browser and go to:
<br>
<br>
`http://localhost:8000`
