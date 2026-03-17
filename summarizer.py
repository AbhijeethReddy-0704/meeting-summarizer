import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an expert meeting analyst.
Your job is to extract structured information from meeting transcripts.

CRITICAL: You must respond with ONLY valid JSON. No explanation,
no markdown, no code fences. Just the raw JSON object.

Use this exact schema:
{
  "summary": "string",
  "key_decisions": ["string"],
  "action_items": [
    {"task": "string", "owner": "string", "deadline": "string or null"}
  ],
  "follow_up_questions": ["string"],
  "sentiment": "positive | neutral | negative"
}

If information is missing, use empty arrays or null.
Never invent names or deadlines not mentioned in the transcript."""


def summarize_meeting(transcript: str) -> dict:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Summarize this meeting transcript:\n\n{transcript}"
            }
        ]
    )

    raw = message.content[0].text

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = raw.strip().strip("```json").strip("```").strip()
        return json.loads(cleaned)