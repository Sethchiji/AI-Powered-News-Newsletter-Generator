
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict
from config import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECIPIENT_EMAILS
from pathlib import Path

def render_email_html(items: List[Dict]) -> str:
    # Load inline HTML template
    tpl_path = Path(__file__).parent / "templates" / "email_template.html"
    template = tpl_path.read_text(encoding="utf-8")
    # Build list items
    rows = []
    for it in items:
        rows.append(f'''
        <div class="card">
            <div class="meta">{(it.get("topic") or "").title()} • {it.get("source") or "Unknown source"}</div>
            <h3>{it.get("title") or "Untitled"}</h3>
            <p>{it.get("summary") or ""}</p>
            <a href="{it.get("url") or "#"}" class="btn">Read the full article</a>
        </div>
        ''')
    content = "\n".join(rows)
    return template.replace("{{CONTENT}}", content)

def send_email(items: List[Dict]) -> None:
    if not RECIPIENT_EMAILS:
        print("[send_email] No RECIPIENT_EMAILS configured. Skipping send.")
        return

    #html = render_email_html(items)
    html = render_email_html(items).replace("{{DATE}}", datetime.now().strftime("%B %d, %Y"))
    
    subject = "Your AI‑Powered Daily News Brief"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENT_EMAILS)

    part_html = MIMEText(html, "html", "utf-8")
    msg.attach(part_html)

    print(f"[send_email] Connecting to SMTP {SMTP_HOST}:{SMTP_PORT} as {SMTP_USERNAME} ...")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAILS, msg.as_string())

    print(f"[send_email] Email sent to {len(RECIPIENT_EMAILS)} recipient(s).")
