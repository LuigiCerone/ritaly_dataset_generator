# Caffè Italia daily dataset scraper

This repository contains code for a Python-based web scraper that scrapes comments from the subreddit `r/italy` on Reddit.
The code is contained within the `scraper.py` file, and the required packages for running the script are listed in the requirements.txt file. The  `data` directory contains the output CSV file, where the scraped comments are saved by default.

## Data background

[`r/italy`](https://www.reddit.com/r/italy/) is a subreddit focused on discussions related to Italy, including news, culture, politics, and society.
Users can post and comment on various topics related to Italy, including travel, language, cuisine, and more.
Among the many threads that populate the subreddit, one of the most popular is the daily thread named "Caffè Italia." As the name suggests, this thread is a virtual coffeehouse where users can gather and exchange ideas on a variety of topics.

Every day, a new "Caffè Italia" thread is created, and users are encouraged to participate by sharing their opinions, asking for advice, or simply chatting with others. The topics discussed in this thread can be very diverse, ranging from Italian cuisine and travel to politics, news, and social issues.

The "Caffè Italia" thread provides an informal and friendly space where users can express themselves freely and connect with others who share their interests or concerns. It's a place where they can ask for recommendations on the best places to visit in Italy, share their thoughts on the latest news or events, or discuss cultural topics, such as literature, art, or music.

What makes the "Caffè Italia" thread so unique is its sense of community. Users feel welcome and valued, and they often return to the thread to catch up with the latest discussions or to contribute to ongoing conversations. Many users have formed friendships and connections through the thread, which has become a hub for the `r/italy` community.

In summary, the "Caffè Italia" thread is a daily gathering place for `r/italy` users to engage in conversations, share their experiences, and connect with others. Whether you're a first-time visitor to the subreddit or a seasoned member of the community, you're sure to find something interesting and engaging in the "Caffè Italia" thread.

## Script params

The `cli.py` accepts the following parameters:

| Name           | Default value | Description                                                                         |
|----------------|---------------|-------------------------------------------------------------------------------------|
| `target_date`  | today         | Date for which to carry out scraping of "Caffè Italia" data in format `YYYY-MM-DD`. |
| `search_limit` | 30            | Upper limit on the number of days allowed to search for posts in the past.          |

## Prerequisites

Tested with:

- Python: 3.8.16
- Make 3.81

## How to run

#### Setup venv

Local environment is set up by using [make](https://www.gnu.org/software/make/) tool.

```bash
make
```

#### Run

```bash
source venv/bin/activate
python cli.py --target_date 2023-03-09 --search_limit 5
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
