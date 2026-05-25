# Groq Streaming Chat CLI

A simple terminal-based AI chat application built with Python using the OpenAI SDK and Groq API.

## Features
- Real-time streaming responses
- Conversation memory
- Fast inference using Groq
- Clean CLI experience

## Tech Stack
- Python
- OpenAI SDK
- Groq API
- python-dotenv

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run the app:

```bash
python stream_chat.py
```

## What I Learned
- Streaming LLM responses
- Using OpenAI-compatible APIs
- Managing chat history
- Building interactive CLI apps