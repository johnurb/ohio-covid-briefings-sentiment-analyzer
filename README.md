### Attempt to find any meaningful relationships between COVID-19 cases and sentiment expressed in the Ohio governor's briefings.

Analyze.py: Works with compiled data from Governor's briefings and NYT COVID data.

- clean_texts.py: Cleansup text files of submissions pulled down from Reddit for use in the sentiment extraction module
- covid_stats.py: Pulls down the NYT COVID data
- get_briefings.py: Scrapes a specific Reddit user's submission history to pull down the text contents of his summaries of briefings
- polarities.py: Extracts sentiment information from the cleaned briefings, uses Vader Sentiment package and TextBlob
(https://github.com/cjhutto/vaderSentiment https://textblob.readthedocs.io/en/dev/)

get_briefings -> clean_texts -> [covid_stats <-> polarities] -> Analyze
