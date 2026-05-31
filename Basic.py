from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from finance import (
    calculate_monthly_expense,
    calculate_emergency_fund,
    calculate_monthly_investment
)

from recommendation import (
    
    recommend_fd,
    diversify,
    allocation,
    stock_amount
)

from sentiment import (
    build_market_summary
)

from prompt import (
    build_prompt
)

from llm import (
    generate_llm_response
)
from database import (
    SessionLocal,
    UserRecommendation
)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Input(BaseModel):

    age: int
    income: int
    risk: str
    investment_period: int = Field(
        default=1,
        ge=1,
        le=12
    )


@app.get("/")
def show():

    return {
        "message": "Investment Suggestor Running"
    }


@app.post("/recommend")
def suggestor(x: Input):

    risk = x.risk.lower()
    db=SessionLocal()
    monthly_expense = calculate_monthly_expense(
        x.income
    )

    emergency_fund = calculate_emergency_fund(
        monthly_expense
    )

    monthly_investment = calculate_monthly_investment(
        x.income
    )

    final = allocation(
        risk,
        monthly_investment,
        x.investment_period
    )

    stock_recommendations = diversify(

    risk,

    stock_amount(
        risk,
        monthly_investment,
        x.investment_period
    )
)

    prompt = build_prompt(

        {
            "age": x.age,
            "income": x.income,
            "risk": risk,
            "period":x.investment_period
        },

        final,

        build_market_summary(),

        stock_recommendations
    )
    suggest=generate_llm_response(
            prompt
        )
    entry=UserRecommendation(
        age=x.age,

        income=x.income,

        risk=risk,

        investment_period=x.investment_period,

        allocation=str(final),

        llm_response=suggest
    )
    db.add(entry)
    db.commit()
    db.close()

    return {

        "risk_profile": risk,

        "financial_summary": {

            "monthly_income": x.income,

            "monthly_expense": monthly_expense,

            "emergency_fund": emergency_fund,

            "monthly_investment": monthly_investment
        },

        "allocation": final,

        "recommended_assets": stock_recommendations,

        "suggestion":suggest
    }