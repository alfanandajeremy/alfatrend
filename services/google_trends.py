from pytrends.request import TrendReq

def get_google_trends():

    pytrends = TrendReq(
        hl='id-ID',
        tz=360
    )

    try:

        trending = pytrends.today_searches(
            pn='ID'
        )

        return trending.tolist()

    except Exception as e:

        return [
            f"Google Trends Error: {e}"
        ]