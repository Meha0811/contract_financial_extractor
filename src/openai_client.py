# src/openai_client.py
from dotenv import load_dotenv
import os
import time
import logging
import openai
import json
import re
import ast

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_chatgpt_system_user(
    system_prompt: str,
    user_prompt: str,
    model: str = None,
    max_tokens: int = 1500,
    retries: int = 3,
):
    """
    Call the OpenAI ChatCompletion endpoint with retries.
    Returns the entire response object.
    """
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-16k")

    for attempt in range(retries):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=max_tokens,
            )
            return resp
        except Exception as e:
            logging.warning(
                f"OpenAI API error (attempt {attempt+1}/{retries}): {e}"
            )
            time.sleep(2 * (attempt + 1))

    raise RuntimeError("OpenAI API failed after retries")


def extract_json_from_response(text: str):
    """
    Try to robustly extract a JSON object from a model response text.
    Returns dict if successful, otherwise None.
    """
    # Try plain JSON
    try:
        return json.loads(text)
    except Exception:
        pass

    # Find first '{' and last '}' and try to parse
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        # quick fixes for trailing commas
        candidate = re.sub(r",\s*}\s*$", "}", candidate)
        candidate = re.sub(r",\s*\]", "]", candidate)
        try:
            return json.loads(candidate)
        except Exception:
            try:
                return ast.literal_eval(candidate)
            except Exception:
                return None

    return None
