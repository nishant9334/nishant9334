"""Step 5a - scrape your public contribution calendar (no token needed).

Usage:  GITHUB_USER=<username> python scripts/fetch_contributions.py
Inside GitHub Actions the username is picked up automatically.
"""
import json, os, re, sys
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GITHUB_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER")
if not USER:
    sys.exit("Set GITHUB_USER to your GitHub username first.")

URL = f"https://github.com/users/{USER}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"


def fetch_html() -> str:
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (profile-readme-bot)"}, timeout=30)
    r.raise_for_status()
    return r.text


def parse(html: str):
    soup = BeautifulSoup(html, "html.parser")
    counts = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"\s*(No|\d[\d,]*)\s+contribution", tip.get_text())
        if m and tip.get("for"):
            counts[tip["for"]] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))
    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        d = td.get("data-date")
        if not d:
            continue
        level = int(td.get("data-level", 0))
        c = counts.get(td.get("id"))
        if c is None:
            c = 0 if level == 0 else level  # fallback if tooltips are missing
        days.append({"date": d, "count": c, "level": level})
    days.sort(key=lambda x: x["date"])
    return days


def stats(days):
    total = sum(d["count"] for d in days)
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    # current streak: count back from the latest day (skip today if still empty)
    current, i = 0, len(days) - 1
    if i >= 0 and days[i]["count"] == 0:
        i -= 1
    while i >= 0 and days[i]["count"] > 0:
        current += 1
        i -= 1
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    monthly = {}
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    return {"total": total, "current_streak": current, "longest_streak": longest,
            "best_day": best, "monthly": monthly}


if __name__ == "__main__":
    days = parse(fetch_html())
    if not days:
        sys.exit("No contribution cells found - check the username / GitHub markup.")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"user": USER, "days": days, "stats": stats(days)}, indent=2))
    print(f"Wrote {OUT} ({len(days)} days, {sum(d['count'] for d in days)} contributions)")
