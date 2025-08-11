import os
import logging
from typing import List

from openai import OpenAI
from dotenv import load_dotenv


logger = logging.getLogger("app.services.ai")


def _get_client() -> OpenAI:
    # Load variables from .env if present
    load_dotenv()
    raw_api_key = os.getenv("OPENAI_API_KEY")
    if not raw_api_key:
        logger.error("OPENAI_API_KEY is not set; cannot initialize OpenAI client")
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    api_key = raw_api_key.strip()
    if api_key != raw_api_key:
        logger.warning("OPENAI_API_KEY contained surrounding whitespace; stripping")
    if any(ch in raw_api_key for ch in ("\n", "\r", "\t")):
        logger.warning("OPENAI_API_KEY contained control whitespace characters (e.g., newline)")
    logger.debug("OpenAI client initialized (api key present: %s)", bool(api_key))
    return OpenAI(api_key=api_key)


SYSTEM_PROMPT = (
    "You are an assistant that extracts concise, actionable action items from a meeting or note description. "
    "Return 3-7 bullet points. Each item should be a short imperative sentence."
)


def generate_action_items(description: str) -> List[str]:
    """Generate action items from a free-form description using OpenAI GPT-4o.

    Returns a list of short strings. Falls back to an empty list on parsing issues.
    """
    client = _get_client()

    logger.info(
        "Generating action items via OpenAI (desc_len=%d)",
        len(description or ""),
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Description:\n" + description + "\n\n"
                        "Extract only the action items as a JSON array of strings."
                    ),
                },
            ],
            temperature=0.3,
        )
    except Exception:
        logger.exception("OpenAI chat.completions.create failed")
        raise

    content = response.choices[0].message.content or "[]"

    # Try to parse a JSON array from the model's content
    import json

    try:
        data = json.loads(content)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            logger.debug("Parsed JSON array from model response (count=%d)", len(data))
            return data
    except Exception:
        logger.debug("Model response was not valid JSON array; falling back to line split")

    # Fallback: split lines if model responded with bullets
    lines = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
    lines = [line for line in lines if line]
    logger.debug("Returning %d items from fallback parsing", len(lines[:7]))
    return lines[:7]


def generate_note_fields(description: str) -> dict:
    """Infer a full note payload from a description using GPT-4o.

    Returns dict with keys: title (str), status (str), date (ISO8601 str), action_items (List[str]).
    """
    client = _get_client()
    logger.info("Generating full note fields via OpenAI (desc_len=%d)", len(description or ""))
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You extract structured note fields from a free-form description. "
                        "Return strictly valid JSON with keys: title (short phrase), status (one of: open, in_progress, done), "
                        "date (ISO8601), action_items (array of 3-7 short strings)."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Description:\n" + description + "\n\n"
                        "Return only JSON, no markdown wrapper."
                    ),
                },
            ],
            temperature=0.3,
        )
    except Exception:
        logger.exception("OpenAI chat.completions.create failed for note fields")
        raise

    content = response.choices[0].message.content or "{}"
    import json

    try:
        data = json.loads(content)
        title = str(data.get("title") or "Untitled")
        status = str(data.get("status") or "open")
        date = str(data.get("date") or "")
        action_items = data.get("action_items") or []
        if not isinstance(action_items, list):
            action_items = []
        action_items = [str(x) for x in action_items][:7]
        return {
            "title": title,
            "status": status,
            "date": date,
            "action_items": action_items,
        }
    except Exception:
        logger.debug("Model response not strict JSON; falling back to minimal fields")
        return {
            "title": description.split(".\n")[0][:60] if description else "Untitled",
            "status": "open",
            "date": "",
            "action_items": generate_action_items(description),
        }


