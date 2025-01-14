import os
import praw
import sqlite3
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent="USERAGENT",
)

connection = sqlite3.connect("database.db")
cursor = connection.cursor()

for submission in reddit.front.hot():
    url = submission.url
    url_end = url[-5:]
    if ".png" in url_end or ".jpeg" in url_end or ".gif" in url_end:
        upvotes = round(submission.upvote_ratio * submission.score / (2 * submission.upvote_ratio - 1))
        downvotes = upvotes - submission.score
        insert_query = """
        INSERT INTO posts (id, created_utc, subreddit, title, upvotes, downvotes, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        values = (submission.id, submission.created_utc, str(submission.subreddit), submission.title, upvotes, downvotes, url)
        try:
            cursor.execute(insert_query, values)
        except sqlite3.IntegrityError:
            pass

delete_query = """
DELETE FROM posts
WHERE created_utc <= strftime('%s', 'now') - (2 * 24 * 60 * 60);
"""

cursor.execute(delete_query)

connection.commit()
connection.close()
