import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

INSIGHTS_TEMPLATE = """
You are a personal finance advisor. Analyse the following financial summary
and provide 5 specific, actionable insights. Be direct and practical.
Use Indian Rupees (₹) in your response.

FINANCIAL SUMMARY:
- Period: {date_range}
- Total Income: ₹{total_income:,.0f}
- Total Expenses: ₹{total_expense:,.0f}
- Net Savings: ₹{net_savings:,.0f}
- Savings Rate: {savings_rate}%
- Highest Spending Category: {top_category} (₹{top_category_amt:,.0f})
- Total Transactions: {num_transactions}

CATEGORY BREAKDOWN:
{category_breakdown}

Provide exactly 5 insights in this format:
1. [insight title]: [specific advice with numbers]
2. [insight title]: [specific advice with numbers]
3. [insight title]: [specific advice with numbers]
4. [insight title]: [specific advice with numbers]
5. [insight title]: [specific advice with numbers]

Be specific. Reference actual numbers from the data. No generic advice.
"""

INSIGHTS_PROMPT = PromptTemplate(
    input_variables=[
        "date_range", "total_income", "total_expense",
        "net_savings", "savings_rate", "top_category",
        "top_category_amt", "num_transactions", "category_breakdown",
    ],
    template=INSIGHTS_TEMPLATE,
)


def generate_insights(summary: dict, category_breakdown) -> str:
    """Generate AI financial insights using Groq Llama 3."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "GROQ_API_KEY not set. Add it to your .env file."

    breakdown_str = "\n".join([
        f"- {row['category']}: ₹{row['amount']:,.0f} ({row['percentage']}%)"
        for _, row in category_breakdown.iterrows()
    ])

    llm = ChatGroq(
        groq_api_key=api_key,
        model_name="llama3-8b-8192",
        temperature=0.4,
    )
    chain = LLMChain(llm=llm, prompt=INSIGHTS_PROMPT)
    return chain.run(
        date_range=summary["date_range"],
        total_income=summary["total_income"],
        total_expense=summary["total_expense"],
        net_savings=summary["net_savings"],
        savings_rate=summary["savings_rate"],
        top_category=summary["top_category"],
        top_category_amt=summary["top_category_amt"],
        num_transactions=summary["num_transactions"],
        category_breakdown=breakdown_str,
    )