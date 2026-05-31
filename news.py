from newsapi import NewsApiClient

newsapi = NewsApiClient(
    api_key="f67923b4621a4c1c9bb45a0c3054b778"
)


def get_market_news():

    articles = newsapi.get_everything(

        q="stock market OR economy OR finance OR gold OR investment",

        language="en",

        sort_by="publishedAt",

        page_size=10
    )

    news_list = []

    for article in articles["articles"]:

        news_list.append({

            "text":

            article["title"] + " " +

            str(article["description"])
        })

    return news_list