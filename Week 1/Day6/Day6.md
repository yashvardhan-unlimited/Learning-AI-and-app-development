# Structured JSON Extractor CLI

## Project

A Python CLI tool that takes unstructured text and converts it into structured JSON using LLM APIs.

---

# Features

- Extract action items from meeting notes
- Return clean structured JSON
- Compare OpenAI and Anthropic SDKs
- Practice JSON prompting and schema design

---

# Concepts Practiced

## Structured Output
Generating predictable JSON responses from LLMs.

## Prompt Engineering
Designing prompts for accurate extraction.

## API Integration
Using both OpenAI and Anthropic SDKs.

## Validation
Ensuring consistent JSON structure.

---

# Installation

```bash
pip install openai anthropic python-dotenv
```

---

# Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

---

# Run the Project

```bash
python action_item_extractor.py
```

---

# Deliverable

- `action_item_extractor.py`
- `README.md`