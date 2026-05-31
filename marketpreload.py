import json
import yfinance as yf

from asset import ALL_STOCKS

market_cache = {}

for stock in ALL_STOCKS:

    try:

        data = yf.download(
            stock,
            period="1y",
            auto_adjust=True,
            progress=False
        )

        close = data["Close"].squeeze()

        returns = (
            close.iloc[-1] -
            close.iloc[0]
        ) / close.iloc[0]

        volatility = (
            close.pct_change()
            .dropna()
            .std()
        )

        score = returns - volatility

        market_cache[stock] = {

            "price": round(
                float(close.iloc[-1]),
                2
            ),

            "returns": round(
                float(returns * 100),
                2
            ),

            "volatility": round(
                float(volatility * 100),
                2
            ),

            "score": round(
                float(score * 100),
                2
            )
        }

    except Exception as e:

        print(stock, e)

with open(
    "market_cache.json",
    "w"
) as f:

    json.dump(
        market_cache,
        f,
        indent=4
    )

print("Cache Updated")