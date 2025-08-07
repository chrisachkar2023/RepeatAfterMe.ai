# RepeatAfterMe.ai

**RepeatAfterMe.ai** is a full-stack web application that helps users improve their English pronunciation through interactive learning and LLMs. Whether you're a beginner or looking to sharpen your skills, this app offers a simple, engaging way to practice and learn how to spell words correctly.

---

## Features

- Displays words for users to pronounce, with varying difficulties
- Records voice input directly in the browser
- Scores pronunciation with AI models
- Button to save words for users to practice later
- Saves recent word history
- Easy deployment with Docker

---

## How to Run

### Prerequisites

- Docker Desktop
- PostgreSQL URL (e.g., Supabase)
- Google Gemini API Key


### Running With Docker

Build the Docker image
```
docker build -t repeatafterme .
```
Run the Docker image
```
docker run -p 8000:8000 \
  -e GEMINI_API_KEY="your_google_gemini_key" \
  -e DATABASE_URL="your_postgres_connection_url" \
  repeatafterme
```
