async function getRecommendation() {

    const age = document.getElementById("age").value;
    const income = document.getElementById("income").value;
    const risk = document.getElementById("risk").value;
    const investment_period = document.getElementById("period").value;

    try {

        const response = await fetch(
            "https://investment-suggestor-for-beginners-production.up.railway.app/recommend",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    age: Number(age),
                    income: Number(income),
                    risk: risk,
                    investment_period: Number(investment_period)
                })
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();

        console.log(data);

        document.getElementById("output").innerHTML = `
            <h2>Financial Summary</h2>

            <p>
                Monthly Income:
                ${data.financial_summary.monthly_income}
            </p>

            <p>
                Monthly Expense:
                ${data.financial_summary.monthly_expense}
            </p>

            <p>
                Monthly Investment:
                ${data.financial_summary.monthly_investment}
            </p>

            <p>
                Emergency Fund:
                ${data.financial_summary.emergency_fund}
            </p>

            <h2>Allocation</h2>

            <pre>${JSON.stringify(data.allocation, null, 2)}</pre>

            <h2>Recommended Stocks</h2>

            <pre>${JSON.stringify(data.recommended_assets, null, 2)}</pre>

            <h2>AI Suggestion</h2>

            <p>${data.suggestion}</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("output").innerHTML = `
            <h2>Error</h2>
            <p>${error.message}</p>
        `;
    }
}