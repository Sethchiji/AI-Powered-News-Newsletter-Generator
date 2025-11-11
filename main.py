
from fetch_news import get_news
from summarize import summarize_articles
from send_email import send_email, render_email_html
from pathlib import Path
from datetime import datetime

def main():
    articles = get_news()
    if not articles:
        print("[main] No articles fetched. Tip: run run_demo.py for an offline demo.")
        return

    summarized = summarize_articles(articles)

    # Save a local HTML preview (useful proof for the demo, even if email fails)
    html = render_email_html(summarized).replace("{{DATE}}", datetime.now().strftime("%B %d, %Y"))
    Path("newsletter_preview.html").write_text(html, encoding="utf-8")
    print("[main] newsletter_preview.html written.")

    # Send the email
    send_email(summarized)

if __name__ == "__main__":
    main()
