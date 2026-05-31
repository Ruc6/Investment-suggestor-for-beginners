from transformers import pipeline

from news import get_market_news

classifier = pipeline(

    "sentiment-analysis",

    model="ProsusAI/finbert"
)


def analysetext(text):

    result = classifier(text)

    return result


def build_market_summary():

    news = get_market_news()

    positive = 0

    negative = 0

    neutral = 0

    summary = []

    for article in news:

        result = analysetext(
            article["text"]
        )[0]

        label = result[
            "label"
        ].lower()

        if label == "positive":

            positive += 1

        elif label == "negative":

            negative += 1

        else:

            neutral += 1

        summary.append({

            "news": article,

            "sentiment": label
        })

    return {

        "positive_news": positive,

        "negative_news": negative,

        "neutral_news": neutral,

        "news_analysis": summary
    }