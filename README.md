
# AI-Powered News Newsletter Generator

A clean, modular Python project that:
1) Fetches the latest news by topic (NewsAPI).
2) Summarizes each article with an LLM (OpenAI).
3) Sends a neat HTML email with links to the full articles.
4) Includes a *no-API demo mode* so you can present even if keys or network fail.

---

## Project Structure

```
ai_newsletter_project/
├── .env.example
├── README.md
├── requirements.txt
├── config.py
├── fetch_news.py
├── summarize.py
├── send_email.py
├── main.py
├── run_demo.py
├── templates/
│   └── email_template.html
└── data/
    └── sample_articles.json
```

---

## Quick Start

### 0) Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure environment
Copy `.env.example` to `.env` and fill in your keys and email settings:
- `NEWSAPI_KEY` — from https://newsapi.org/
- `OPENAI_API_KEY` — from https://platform.openai.com/
- SMTP settings — either Gmail (with App Password) or your provider/SendGrid SMTP.

> **Gmail users:** You must create an App Password (2FA required). See: https://support.google.com/accounts/answer/185833

### 3) Run the full pipeline
```bash
python main.py
```
This will:
- Fetch latest articles on your chosen topics
- Summarize with OpenAI
- Email the formatted newsletter

### 4) No‑API demo (for class presentation)
If you don’t have keys ready or the network is flaky, run:
```bash
python run_demo.py
```
This will:
- Load a small sample dataset (no network needed)
- Use a simple built-in summarizer
- Generate a **newsletter_preview.html** file for you to open and show

Output path: `newsletter_preview.html` (same folder).

---

## Scheduling (Automation)

### Windows Task Scheduler
- Action: *Start a program* → `python`
- Arguments: `C:\path\to\main.py`
- Start in: `C:\path\to\ai_newsletter_project`
- Trigger: Daily at 8:00 AM

### macOS/Linux (cron)
Run `crontab -e` and add (daily at 8:00 AM):
```
0 8 * * * cd /path/to/ai_newsletter_project && /path/to/python main.py
```

> Ensure your virtual environment path and environment variables are available to cron/Task Scheduler (you can call a wrapper shell script that activates your venv and exports keys).

---

## Troubleshooting (what to say if something breaks)

- **API errors / 401**: Key missing or invalid → check `.env` variables are loaded.
- **Network timeouts**: Show `run_demo.py` to prove your pipeline logic without internet.
- **SMTP auth failed**: If using Gmail, you likely need an **App Password**. Regular password won’t work.
- **Rate limits**: Reduce number of articles or topics in `config.py`.

---

## Rubric Alignment Cheat Sheet (for your demo)

1. **Fetching Data** → run `main.py` and show terminal logs printing headlines and URLs.
2. **Summarizing** → point to `summarize.py` and show console summaries (we print the first ~200 chars).
3. **Email** → Open inbox; show the received newsletter with clickable links and clean formatting.
4. **Automation** → reference the “Scheduling” section above; optionally show your Task Scheduler/cron entry.
5. **Understanding** → be ready to point to functions in each file and explain their role in the pipeline.

Good luck!
