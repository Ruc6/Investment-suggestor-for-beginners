from rag import retrieve_context


def build_prompt(

    user_data,

    allocation,

    market_context,

    stock_recommendations
):

    query = (

        f"User allocations as {allocation} "
        f"and these stock allotment "
        f"{stock_recommendations}"
    )

    context = retrieve_context(
        query
    )
   
    prompt = f"""

USER PROFILE:
{user_data}

PORTFOLIO ALLOCATION:
{allocation}

RECOMMENDED STOCKS:
{stock_recommendations}

CURRENT MARKET TOP NEWS:
{market_context}

FINANCIAL KNOWLEDGE:
{context}

Analyze this portfolio.

Explain:
Answer in short to the point single liners
- risks associated
- inflation impact
- improvements
-feasibility of these investments in current market situation
-estimeted amount returns after given period 

If some allocations are risky,
suggest safer alternatives.
"""

    return prompt