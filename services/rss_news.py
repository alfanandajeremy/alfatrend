import feedparser

RSS_LIST = [

    "https://rss.cnnindonesia.com/rss/cnnindonesia",

    "https://rss.tempo.co/nasional",

    "https://www.antaranews.com/rss/terkini.xml"
]


def get_news():

    headlines = []

    for url in RSS_LIST:

        try:

            feed = feedparser.parse(url)

            for entry in feed.entries[:10]:

                headlines.append(
                    entry.title
                )

        except Exception:
            pass

    return headlines