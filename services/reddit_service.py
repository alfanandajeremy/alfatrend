import praw


def get_reddit_trends():

    reddit = praw.Reddit(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        user_agent="trend-intelligence"
    )

    subreddits = [
        "indonesia",
        "technology",
        "worldnews"
    ]

    posts = []

    for sub in subreddits:

        subreddit = reddit.subreddit(sub)

        for post in subreddit.hot(limit=10):

            posts.append(post.title)

    return posts
