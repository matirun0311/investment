#!/usr/bin/env python3
"""次の週の記事の下書きを _posts/ に作成する。

最新の記事の翌週月曜日を公開日とし、カリキュラム (curriculum.md) から
該当する週のテーマを取り出してテンプレートに埋め込む。

使い方:
    python3 scripts/new_article.py <slug>
    例: python3 scripts/new_article.py three-ways-to-profit
"""
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
POST_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-.+\.md$")
CURRICULUM_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|$")


def latest_post():
    posts = sorted(p for p in POSTS.glob("*.md") if POST_NAME.match(p.name))
    if not posts:
        sys.exit("_posts/ に記事がありません")
    return posts[-1]


def curriculum_titles():
    titles = {}
    for line in (ROOT / "curriculum.md").read_text(encoding="utf-8").splitlines():
        m = CURRICULUM_ROW.match(line)
        if m:
            titles[int(m.group(1))] = m.group(2)
    return titles


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"[a-z0-9-]+", sys.argv[1]):
        sys.exit("使い方: python3 scripts/new_article.py <slug（半角英小文字・数字・ハイフン）>")
    slug = sys.argv[1]

    last = latest_post()
    last_date = datetime.date.fromisoformat(POST_NAME.match(last.name).group(1))
    last_week = int(re.search(r"^week:\s*(\d+)", last.read_text(encoding="utf-8"), re.M).group(1))

    week = last_week + 1
    date = last_date + datetime.timedelta(days=7 - last_date.weekday())  # 翌週の月曜日
    titles = curriculum_titles()
    if week not in titles:
        sys.exit(f"カリキュラムに第{week}週がありません")

    path = POSTS / f"{date.isoformat()}-{slug}.md"
    if path.exists():
        sys.exit(f"{path} はすでに存在します")

    next_title = titles.get(week + 1, "（未定）")
    body = (ROOT / "templates" / "article-template.md").read_text(encoding="utf-8")
    body = (
        body.replace("【第N週】タイトル", f"【第{week}週】{titles[week]}")
        .replace("YYYY-MM-DD", date.isoformat())
        .replace("week: N", f"week: {week}")
        .replace("第N+1週）は「次回のテーマ」", f"第{week + 1}週）は「{next_title}」")
    )
    path.write_text(body, encoding="utf-8")
    print(f"作成しました: {path.relative_to(ROOT)}（第{week}週・{date} 公開）")


if __name__ == "__main__":
    main()
