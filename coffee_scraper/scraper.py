import logging
import os
import sys
from typing import Tuple, Union

import pandas as pd
import pendulum
from dotenv import find_dotenv, load_dotenv
from praw import Reddit
from praw.models import Submission, Subreddits


def get_reddit_client() -> Reddit:
    logging.debug("Initializing Reddit client.")

    client_id = os.getenv("CLIENT_ID")
    secret_token = os.getenv("SECRET_TOKEN")

    # Create reddit read-only client
    return Reddit(
        client_id=client_id,
        client_secret=secret_token,
        user_agent="ritaly_bot/1.0.0",
    )


def get_subreddit(reddit: Reddit) -> Subreddits:
    logging.debug("Get r/italy subreddit.")
    # Get r/italy reddit instance
    return reddit.subreddit("italy")


def get_coffee_post(
    ritaly: Subreddits, target_date: pendulum, search_limit: int
) -> Tuple[pd.Series, Union[Submission, None]]:
    post_info_series: pd.Series = pd.Series(dtype=object)

    for submission in ritaly.search(
        'flair:"caffè italia"', limit=search_limit, sort="new"
    ):
        if (
            submission.link_flair_text == "Caffè Italia"
            and pendulum.from_timestamp(submission.created_utc).date() == target_date
        ):
            post_info_series = pd.Series(
                {
                    "post_subreddit": submission.subreddit,
                    "post_title": submission.title,
                    "post_selftext": submission.selftext,
                    "post_upvote_ratio": submission.upvote_ratio,
                    "post_ups": submission.ups,
                    "post_downs": submission.downs,
                    "post-score": submission.score,
                    "post_created_at": pendulum.from_timestamp(submission.created_utc),
                }
            )
            return post_info_series, submission

    return post_info_series, None


def get_all_comments(italy_coffe_submission: Submission) -> pd.DataFrame:
    comment_info = []

    logging.debug("Start expanding comments tree for coffee post")
    italy_coffe_submission.comments.replace_more(limit=None)

    for comment in italy_coffe_submission.comments.list():
        comment_info.append(
            {
                "comment_author": comment.author,
                "comment_author_flair_text": comment.author_flair_text,
                "comment_created_at": pendulum.from_timestamp(comment.created_utc),
                "comment_body": comment.body,
                "comment_edited": bool(comment.edited),
                "comment_distinguished": bool(comment.distinguished),
                "comment_id": comment.id,
                "comment_parent_id": comment.parent_id,
                "comment_score": comment.score,
                "comment_ups": comment.ups,
                "comment_downs": comment.downs,
                "comment_num_comments": len(comment.replies),
                "comment_is_submitter": comment.is_submitter,
                "comment_num_reports": comment.num_reports,
            }
        )

    return pd.DataFrame.from_records(comment_info)


def merge_info(post_series: pd.Series, comments_df: pd.DataFrame) -> pd.DataFrame:
    for col, val in post_series.items():
        comments_df[col] = val

    return comments_df


def write_csv(df_out: pd.DataFrame, target_date: pendulum) -> None:
    parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logging.debug(
        'Saving result to file "%s/data/coffee-italy-%s.csv"',
        parent_path,
        target_date.to_date_string(),
    )
    df_out.to_csv(
        f"{parent_path}/data/coffee-italy-{target_date.to_date_string()}.csv",
        index=False,
    )


def main(target_date: pendulum, search_limit: int):
    load_dotenv(find_dotenv())

    logging.debug("Scraping for r/italy coffee post for date: %s", target_date)

    client = get_reddit_client()

    subreddit = get_subreddit(client)

    post_info, post_submission = get_coffee_post(
        subreddit, target_date=target_date, search_limit=search_limit
    )

    if len(post_info) == 0:
        logging.error("r/italy coffee post not found for the requested date!")
        sys.exit(1)

    comments_info = get_all_comments(post_submission)

    final_df = merge_info(post_info, comments_info)

    write_csv(final_df, target_date=target_date)
