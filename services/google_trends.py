from pytrends.request import TrendReq
import pandas as pd


def get_google_trends():

    try:

        pytrends = TrendReq(
            hl='id-ID',
            tz=360
        )

        # ====================================
        # GOOGLE TRENDING SEARCHES
        # ====================================
        trending = pytrends.trending_searches(
            pn='indonesia'
        )

        # ====================================
        # CONVERT TO LIST
        # ====================================
        if isinstance(trending, pd.DataFrame):

            trends = trending[0].tolist()

        else:

            trends = list(trending)

        # ====================================
        # CLEAN DATA
        # ====================================
        cleaned = []

        for trend in trends:

            trend = str(trend).strip()

            if (
                len(trend) > 2
                and len(trend) < 100
                and trend not in cleaned
            ):

                cleaned.append(trend)

        # ====================================
        # SAFE FALLBACK
        # ====================================
        if not cleaned:

            return [
                "Indonesia",
                "AI",
                "Bitcoin",
                "Teknologi"
            ]

        return cleaned

    except Exception as e:

        return [
            f"Trend Error: {str(e)}"
        ]
