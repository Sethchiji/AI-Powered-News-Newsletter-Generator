
from typing import List, Dict
from config import OPENAI_API_KEY
import time

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

PROMPT = (
    "You are an assistant that writes tight, neutral news briefs. "
    "Summarize the article below in 2–3 sentences (max 70 words). "
    "Mention the outlet if known and preserve key facts and dates. "
    "End with a 'Read more' cue."
)

def _client():
    if not OPENAI_API_KEY or OpenAI is None:
        return None
    return OpenAI(api_key=OPENAI_API_KEY)

def summarize_articles(articles: List[Dict]) -> List[Dict]:
    client = _client()
    summarized = []

    for idx, a in enumerate(articles):
        text = a.get("description") or a.get("content") or a.get("title", "")
        model_summary = None

        if client is not None and text:
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": PROMPT},
                        {"role": "user", "content": f"Title: {a.get('title')}\nSource: {a.get('source')}\nURL: {a.get('url')}\nText: {text}"}
                    ],
                    temperature=0.3,
                    max_tokens=140,
                )
                model_summary = resp.choices[0].message.content.strip()
            except Exception as e:
                print(f"[summarize] OpenAI error on article {idx}: {e}. Falling back.")
                model_summary = None
                time.sleep(0.5)

        if not model_summary:
            # Fallback concise summary
            title = (a.get("title") or "Untitled").strip()
            source = a.get("source") or "Unknown outlet"
            model_summary = f"{title} — {source}. Key highlights reported in the linked article. Read more for details."

        out = dict(a)
        out["summary"] = model_summary
        summarized.append(out)
        print(f"[summarize] {idx+1}/{len(articles)} summarized.")

    return summarized
