import json

with open(
    "market_cache.json",
    "r"
) as f:

    MARKET_DATA = json.load(f)


def rank_assets(asset_list):

    ranked = []

    for stock in asset_list:

        if stock in MARKET_DATA:

            ranked.append(

                (
                    stock,
                    MARKET_DATA[stock]
                )
            )

    ranked.sort(

        key=lambda x:
        x[1]["score"],

        reverse=True
    )

    return ranked