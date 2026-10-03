#!/usr/bin/env python3
"""公開日を迎えた記事を、自分の Gmail 宛てにメールで送る。

GitHub Actions の週次ワークフローから実行される。送信元・宛先はどちらも
環境変数 GMAIL_ADDRESS（Gmail のアプリパスワードは GMAIL_APP_PASSWORD）。

使い方:
    python3 scripts/send_email.py                # 今日（JST）が公開日の記事を送る
    python3 scripts/send_email.py --latest       # 今日以前で最新の記事を送る（送信テスト用）
    python3 scripts/send_email.py --date 2026-10-05 --dry-run   # 送らずに .eml を書き出す
"""
import argparse
import datetime
import os
import re
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo

import markdown

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
POST_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)\.md$")
SITE_TITLE = "週刊・はじめての株式投資"

STYLE = """
body { font-family: -apple-system, 'Hiragino Sans', 'Noto Sans JP', sans-serif; line-height: 1.8; color: #222; max-width: 680px; margin: 0 auto; padding: 16px; }
h1 { font-size: 1.4em; } h2 { font-size: 1.15em; border-left: 4px solid #2a7ae2; padding-left: 8px; margin-top: 1.8em; }
table { border-collapse: collapse; margin: 1em 0; } th, td { border: 1px solid #ccc; padding: 6px 10px; } th { background: #f3f6fa; }
blockquote { color: #555; border-left: 3px solid #ddd; margin: 0; padding-left: 12px; }
.link { margin-top: 2em; font-size: 0.9em; }
"""


def load_posts():
    posts = []
    for path in sorted(POSTS.glob("*.md")):
        m = POST_NAME.match(path.name)
        if not m:
            continue
        text = path.read_text(encoding="utf-8")
        _, front, body = text.split("---", 2)
        meta = dict(
            (k.strip(), v.strip().strip('"'))
            for k, v in (line.split(":", 1) for line in front.strip().splitlines() if ":" in line)
        )
        posts.append({
            "date": datetime.date.fromisoformat(m.group(1)),
            "slug": m.group(2),
            "title": meta["title"],
            "body": body.strip(),
        })
    return posts


def pick_post(posts, date, latest):
    if latest:
        candidates = [p for p in posts if p["date"] <= date]
        return candidates[-1] if candidates else None
    return next((p for p in posts if p["date"] == date), None)


def build_message(post, address, site_url):
    url = None
    if site_url:
        d = post["date"]
        url = f"{site_url.rstrip('/')}/{d:%Y/%m/%d}/{post['slug']}/"

    html_body = markdown.markdown(post["body"], extensions=["tables"])
    link_html = f'<p class="link">サイトで読む: <a href="{url}">{url}</a></p>' if url else ""
    html = (
        f"<!doctype html><html><head><meta charset='utf-8'><style>{STYLE}</style></head>"
        f"<body><h1>{post['title']}</h1>{html_body}{link_html}</body></html>"
    )
    text = f"{post['title']}\n\n{post['body']}\n"
    if url:
        text += f"\nサイトで読む: {url}\n"

    msg = EmailMessage()
    msg["Subject"] = f"【{SITE_TITLE}】{post['title']}"
    msg["From"] = f"{SITE_TITLE} <{address}>"
    msg["To"] = address
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")
    return msg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--latest", action="store_true", help="今日以前で最新の記事を送る")
    parser.add_argument("--date", help="今日の代わりに使う日付（YYYY-MM-DD）")
    parser.add_argument("--dry-run", action="store_true", help="送信せず .eml を書き出す")
    args = parser.parse_args()

    date = (datetime.date.fromisoformat(args.date) if args.date
            else datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date())
    post = pick_post(load_posts(), date, args.latest)
    if post is None:
        print(f"{date} に送る記事はありません。")
        return

    address = os.environ.get("GMAIL_ADDRESS", "me@example.com" if args.dry_run else "")
    if not address:
        sys.exit("環境変数 GMAIL_ADDRESS が設定されていません")
    msg = build_message(post, address, os.environ.get("SITE_URL", ""))

    if args.dry_run:
        out = Path(os.environ.get("EML_OUT", f"{post['date']}-{post['slug']}.eml"))
        out.write_bytes(bytes(msg))
        print(f"書き出しました: {out}（件名: {msg['Subject']}）")
        return

    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        sys.exit("環境変数 GMAIL_APP_PASSWORD が設定されていません")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(address, password)
        smtp.send_message(msg)
    print(f"送信しました: {msg['Subject']}")


if __name__ == "__main__":
    main()
