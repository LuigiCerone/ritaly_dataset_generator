import praw
import os
import pendulum

import pandas as pd

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

# Create reddit read-only client
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_TOKEN,
    user_agent='ritaly_bot/0.0.1',
)

# Get r/italy reddit istance
ritaly = reddit.subreddit('italy')
post_info_series = None
italy_coffe_submission = None

for submission in ritaly.search('flair:"caffè italia"', limit=5):
    if submission.link_flair_text == 'Caffè Italia' and pendulum.from_timestamp(submission.created_utc).day == pendulum.yesterday().day:
        post_info_series = pd.Series({
            'post_subreddit': submission.subreddit,
            'post_title': submission.title,
            'post_selftext': submission.selftext,
            'post_upvote_ratio': submission.upvote_ratio,
            'post_ups': submission.ups,
            'post_downs': submission.downs,
            'post-score': submission.score,
            'post_created_at': pendulum.from_timestamp(submission.created_utc)
        })
        italy_coffe_submission = submission
        break

if post_info_series is None:
    exit(1)

comment_info = list()

italy_coffe_submission.comments.replace_more(limit=None)

for comment in italy_coffe_submission.comments.list():
    comment_info.append({
            'comment_author': comment.author,
            'comment_created_at': pendulum.from_timestamp(comment.created_utc),
            'comment_body': comment.body,
            'comment_edited': bool(comment.edited),
            'comment_distinguished': bool(comment.distinguished),
            'comment_id': comment.id,
            'comment_parent_id': comment.parent_id,
            'comment_score': comment.score
    })

comment_info_df = pd.DataFrame.from_records(comment_info)

for col, val in post_info_series.items():
    comment_info_df[col] = val

comment_info_df.to_csv('./test_data.csv', index=False)

