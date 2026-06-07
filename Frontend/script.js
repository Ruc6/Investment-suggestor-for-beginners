async function getRecommendation(){
    const age=document.getElementById("age").value;
    const age=document.getElementById("income").value;
    const risk=document.getElementById("risk").value;
    const investment_period=document.getElementById("period").value;
    const response = await fetch(

        "https://investment-suggestor-for-beginners-production.up.railway.app/recommend",

        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },
        
    body:JSON.stringify({

                age: Number(age),

                income: Number(income),

                risk: risk,

                investment_period: Number(period)
            })
        });
        const data = await response.json();
document.getElementById("output").innerHTML = `

        <h2>Financial Summary</h2>

        <p>
            Monthly Investment:
            ${data.financial_summary.monthly_investment}
        </p>

        <h2>Allocation</h2>

        <pre>
${JSON.stringify(data.allocation, null, 2)}
</pre>
<h2> Recommendated stocks</h2>
<p>
${data.recommended_assets}
</p>

        <h2>AI Suggestion</h2>

        <p>
            ${data.suggestion}
        </p>
    `;
}
