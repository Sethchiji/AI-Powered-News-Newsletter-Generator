import requests
from typing import List, Dict
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, USER_AGENT, TOPICS, MAX_ARTICLES_PER_TOPIC

# Try "everything" first; if you still get 401 after this patch, change to top-headlines (see note below)
NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
# NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"  # <- fallback option if your plan requires it

def get_news(topics: List[str] = None, max_per_topic: int = None) -> List[Dict]:
    topics = topics or TOPICS
    max_per_topic = max_per_topic or MAX_ARTICLES_PER_TOPIC

    # --- Debug to confirm key is loaded ---
    print("[debug] NEWSAPI_KEY loaded? ", "yes" if NEWSAPI_KEY else "no")
    if NEWSAPI_KEY:
        print("[debug] NEWSAPI_KEY starts with:", NEWSAPI_KEY[:6], "…")

    if not NEWSAPI_KEY:
        print("[fetch_news] No NEWSAPI_KEY found. Returning empty list (use run_demo.py).")
        return []

    # Use headers for the API key (preferred)
    headers = {
        "User-Agent": USER_AGENT,
        "X-Api-Key": NEWSAPI_KEY,      # <-- KEY GOES IN HEADER
    }

    all_articles = []

    # Prefer last 2 days for freshness (for 'everything' endpoint)
    from_date = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")

    for topic in topics:
        print(f"[fetch_news] Fetching topic '{topic}' ...")

        # Build params WITHOUT apiKey in the URL
        if "top-headlines" in NEWSAPI_URL:
            params = {
                "q": topic,
                "language": "en",
                "pageSize": max_per_topic,
            }
        else:
            params = {
                "q": topic,
                "from": from_date,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": max_per_topic,
            }

        r = requests.get(NEWSAPI_URL, params=params, headers=headers, timeout=20)
        # If this still fails, print body for debugging
        if r.status_code != 200:
            print("[fetch_news][debug] status:", r.status_code, "body:", r.text[:400])
        r.raise_for_status()

        data = r.json()
        articles = data.get("articles", [])
        for a in articles:
            all_articles.append({
                "topic": topic,
                "title": a.get("title") or "(No title)",
                "url": a.get("url"),
                "source": (a.get("source") or {}).get("name"),
                "publishedAt": a.get("publishedAt"),
                "content": a.get("content") or "",
                "description": a.get("description") or "",
            })

    print(f"[fetch_news] Total fetched: {len(all_articles)}")
    return all_articles