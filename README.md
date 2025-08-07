# RepeatAfterMe.ai

**RepeatAfterMe.ai** is a full-stack web application that helps users improve their English pronunciation through LLMs. Whether you're a beginner or looking to sharpen your skills, this app offers a simple, engaging way to practice and learn how to pronounce words correctly.

---

## Features

- Displays words of varying difficulties for users to pronounce
- Records voice input directly in the browser
- Scores pronunciation with AI models
- User account creation
- Allows users to save words to practice later
- Saves recent word history
- Easy deployment with Docker

---

## Prerequisites

- Docker Desktop
- PostgreSQL Connection URL (e.g., Supabase)
- Google Gemini API Key

---

## Running With Docker

Build the Docker image
```
docker build -t repeatafterme .
```
Run the Docker container
```
docker run -p 8000:8000 \
  -e DATABASE_URL="<your_postgres_connection_url>" \
  -e GEMINI_API_KEY="<your_google_gemini_key>" \
  repeatafterme
```

Once the container is running, open your browser and go to:
<br>
<br>
`http://localhost:8000`
