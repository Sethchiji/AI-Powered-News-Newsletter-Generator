
import json
from pathlib import Path
from datetime import datetime
from send_email import render_email_html

def main():
    sample_path = Path(__file__).parent / "data" / "sample_articles.json"
    articles = json.loads(sample_path.read_text(encoding="utf-8"))

    # Create short, friendly summaries without calling an API
    for a in articles:
        title = a.get("title") or "Untitled"
        source = a.get("source") or "Unknown source"
        a["summary"] = f"{title} — {source}. Here are the key points at a glance. Read more for full context."

    html = render_email_html(articles).replace("{{DATE}}", datetime.now().strftime("%B %d, %Y"))
    out = Path("newsletter_preview.html")
    out.write_text(html, encoding="utf-8")
    print(f"[run_demo] Wrote {out.resolve()} — open it in your browser for the presentation.")

if __name__ == "__main__":
    main()
