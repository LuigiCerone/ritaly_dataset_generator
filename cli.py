import argparse
import logging

import pendulum

from coffee_scraper import scraper


def main():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="r/italy reddit scraper")
    parser.add_argument(
        "--target_date",
        type=lambda s: pendulum.from_format(s, "YYYY-MM-DD").date(),
        default=pendulum.now().date(),
        nargs="?",
        help="Target date in string format YYYY-MM-DD",
    )
    parser.add_argument(
        "--search_limit",
        type=int,
        default=30,
        nargs="?",
        help="Upper limit on the number of days allowed to search for posts in the past",
    )
    args = parser.parse_args()
    scraper.main(target_date=args.target_date, search_limit=args.search_limit)


if __name__ == "__main__":
    main()
