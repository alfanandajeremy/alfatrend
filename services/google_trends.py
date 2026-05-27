from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup


def get_google_trends():

    # ====================================
    # METHOD 1 — PYTRENDS
    # ====================================
    try:

        pytrends = TrendReq(
            hl='id-ID',
            tz=360
        )

        trending = pytrends.today_searches(
            pn='ID'
        )

        trends = trending.tolist()

        trends = clean_trends(trends)

        if trends:
            return trends

    except Exception:
        pass

    # ====================================
    # METHOD 2 — SCRAPING FALLBACK
    # ====================================
    try:

        url = (
            "https://trends.google.com/trends/trendingsearches/daily?geo=ID"
        )

        headers = {
            "User-Agent": (
                "Mozilla/5.0"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text()

        trends = []

        for line in text.splitlines():

            line = line.strip()

            if (
                len(line) > 3
                and len(line) < 80
                and "Google" not in line
                and "Trends" not in line
            ):

                trends.append(line)

        trends = clean_trends(trends)

        if trends:
            return trends[:20]

    except Exception:
        pass

    # ====================================
    # METHOD 3 — SAFE FALLBACK
    # ====================================
    return [
        "Indonesia",
        "Teknologi AI",
        "Bitcoin",
        "Timnas Indonesia",
        "IHSG",
        "Startup",
        "DeepSeek",
        "OpenAI",
        "TikTok",
        "YouTube"
    ]


def clean_trends(trends):

    cleaned = []

    for trend in trends:

        trend = str(trend).strip()

        if (
            len(trend) > 2
            and len(trend) < 100
            and trend not in cleaned
        ):

            cleaned.append(trend)

    return cleaned
