from market import rank_assets

import yfinance as yf

from fd import Rates

from asset import (
    ALL_STOCKS
)
import json
from market import rank_assets

def allocation(
    risk,
    monthly_investment,
    investment_period
):

    allocation = {}

    if risk.lower() == "high":

        allocation = {
            "Stocks": 0.50,
            "ETFs": 0.20,
            "Mutual Funds": 0.15,
            "Gold": 0.10,
            "Debt Funds": 0.05
        }

    elif risk.lower() == "medium":

        allocation = {
            "Stocks": 0.35,
            "ETFs": 0.25,
            "Mutual Funds": 0.20,
            "Gold": 0.10,
            "Debt Funds": 0.10
        }

    elif risk.lower() == "low":

        allocation = {
            "Stocks": 0.15,
            "ETFs": 0.20,
            "Mutual Funds": 0.20,
            "Gold": 0.15,
            "FD": 0.20,
            "Debt Funds": 0.10
        }

    else:

        return {
            "error": "Invalid risk profile"
        }

    if investment_period >= 10:

        allocation["Stocks"] += 0.10

        allocation["Debt Funds"] -= 0.05

    elif investment_period <= 3:

        allocation["Gold"] += 0.05

        allocation["FD"] = allocation.get(
            "FD",
            0
        ) + 0.05

        allocation["Stocks"] -= 0.10

    final_allocation = {}

    for asset, percent in allocation.items():

        amount = round(
            monthly_investment * percent,
            2
        )

        final_allocation[asset] = {

            "percentage": round(
                percent * 100,
                2
            ),

            "amount": amount
        }

    return final_allocation


def stock_amount(
    risk,
    monthly_investment,
    investment_period
):

    if risk.lower() == "high":

        stock_percent = 0.50

    elif risk.lower() == "medium":

        stock_percent = 0.35

    elif risk.lower() == "low":

        stock_percent = 0.15

    else:

        return "Invalid risk profile"

    if investment_period >= 10:

        stock_percent += 0.10

    elif investment_period <= 3:

        stock_percent -= 0.10

    stock_amount = (
        monthly_investment * stock_percent
    )

    return round(
        stock_amount,
        2
    )


def recommend_assets(risk):

    ranked = rank_assets(
        ALL_STOCKS
    )

    filtered_assets = []

    for asset in ranked:

        stock_name = asset[0]

        metrics = asset[1]

        volatility = metrics["volatility"]

        if risk == "low":

            if volatility < 2:

                filtered_assets.append(asset)

        elif risk == "medium":

            if volatility < 4:

                filtered_assets.append(asset)

        else:

            filtered_assets.append(asset)

    top_assets = sorted(

        filtered_assets,

        key=lambda x: x[1]["score"],

        reverse=True
    )

    return top_assets[:5]


def recommend_fd(period):

    best_bank = None

    best_rate = 0

    for bank in Rates:

        key = f"{period}_year"

        if key in bank:

            if bank[key] > best_rate:

                best_rate = bank[key]

                best_bank = bank["bank"]

    return {

        "bank": best_bank,

        "interest_rate": best_rate
    }


def hedging(
    top_assets,
    invest_stock
):

    final_allocate = []

    for x in range(
        len(top_assets),
        0,
        -1
    ):

        amount = invest_stock / x

        allocated_sum = 0

        count = 0

        allocation = []

        for asset in top_assets:

            stock_name = asset[0]

            data = yf.download(

                stock_name,

                period="1y"
            )

            current_price = data["Close"].squeeze().iloc[-1]
            if float(current_price) <= amount:

                shares = int(
                    amount / current_price
                )

                invested_amount = (
                    shares * current_price
                )

                allocated_sum += invested_amount

                count += 1

                allocation.append({

                    "stock_name": stock_name,

                    "shares": shares,

                    "invested_amount": round(
                        invested_amount,
                        2
                    )
                })

        if count == x:

            final_allocate = allocation

            break

    return final_allocate
def diversify(
    risk,
    stock_budget
):

    ranked_assets = rank_assets(
        ALL_STOCKS
    )

    filtered = []

    for asset in ranked_assets:

        stock_name = asset[0]

        metrics = asset[1]

        volatility = metrics["volatility"]

        if risk == "low":

            if volatility < 2:
                filtered.append(asset)

        elif risk == "medium":

            if volatility < 4:
                filtered.append(asset)

        else:

            filtered.append(asset)

    affordable = []

    for asset in filtered:

        stock_name = asset[0]

        metrics = asset[1]

        price = metrics["price"]

        if price <= stock_budget:

            affordable.append(asset)

    affordable.sort(

        key=lambda x:
        x[1]["score"],

        reverse=True
    )

    selected = affordable[:5]

    if len(selected) == 0:

        return {

            "error":
            "No affordable stocks found"
        }

    portfolio = []

    remaining_budget = stock_budget

    equal_budget = (
        stock_budget /
        len(selected)
    )

    total_used = 0

    for asset in selected:

        stock_name = asset[0]

        metrics = asset[1]

        price = metrics["price"]

        shares = int(
            equal_budget /
            price
        )

        if shares == 0:
            continue

        invested = (
            shares *
            price
        )

        total_used += invested

        portfolio.append({

            "symbol":
            stock_name,

            "price":
            round(price, 2),

            "shares":
            shares,

            "invested":
            round(
                invested,
                2
            ),

            "score":
            metrics["score"]
        })

    return {

        "budget":
        round(
            stock_budget,
            2
        ),

        "invested":
        round(
            total_used,
            2
        ),

        "cash_left":
        round(
            stock_budget -
            total_used,
            2
        ),

        "portfolio":
        portfolio
    }