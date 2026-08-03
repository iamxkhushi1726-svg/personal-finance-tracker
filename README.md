# 💰 Personal Finance Tracker + AI Insights

> Project 10 · Building a Personal Finance Tracker with AI Insights

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iamxkhushi1726-svg-personal-finance-tracker-app-dquz6d.streamlit.app/)

An enterprise-grade financial intelligence engine that transforms raw transactional data into structured behavioral metrics. The platform pairs high-density data aggregations and interactive **Plotly** data architectures with advanced automated reasoning via **Groq Llama 3** to yield deep, contextual cash flow audits. 

Users can securely parse custom ledger payloads via CSV data streams or run execution instances on sandboxed demo data.

### 🌐 [Explore the Live Production Environment](https://iamxkhushi1726-svg-personal-finance-tracker-app-dquz6d.streamlit.app/)

---

## ⚡ Core Engine Features

* **Multi-Channel Ingestion:** Stream custom raw accounting files via a local browser context or initialize a synthetic sample matrix instantly.
* **Executive Macro Cards:** Real-time calculation grids covering gross capital inflows, operational outflows, net cash retention metrics, and system transaction velocity.
* **High-Density Visualization Matrix:** Implements 4 rich structural chart profiles (Proportional Expense Donut, Linear Category Volume Bar, Daily Liquidity Timeline, and a complex Balance Reconciliation Waterfall).
* **Granular Query Registry:** Deep-index historical database with fast interactive filtering categories and transactional direction selectors.
* **Institutional Audit Generation:** Single-click execution pipeline providing 5 specific, high-context capital optimization strategies anchored directly onto your processed cash parameters.
* **Localization Layer:** Out-of-the-box structural alignment with multi-scale formatting rules for Indian Rupee (`₹`) notation styles.

---

## 🛠️ Technology Stack Architecture

* **Presentation & Interface Engine:** Streamlit (Custom UI Injection Engine via HTML/CSS overrides)
* **Data Layouts & Mathematical Modeling:** pandas, NumPy
* **Interactive Graphics Pipeline:** Plotly Graph Objects (go) & Express (px)
* **Language Execution Interface:** LangChain Engine Framework
* **Inference Compute Layer:** Groq Hardware Acceleration API (Llama 3 Model Core)

---

## 📋 Data Schema Interface

To ingest your custom accounts ledger seamlessly, structure your source dataset to align with the following standard columns:

```csv
date,description,category,amount,type
2026-05-01,Corporate Salary,Income,45000,income
2026-05-02,Vendor Payment,Food,450,expense
```

## Tech Stack

Python · Streamlit · Plotly · LangChain · Groq (Llama 3) · pandas

## CSV Format

```
date,description,category,amount,type
2026-05-01,Salary Credit,Income,45000,income
2026-05-02,Zomato Order,Food,450,expense
```

## Run Locally

```bash
git clone https://github.com/iamxkhushi1726-svg/personal-finance-tracker.git
cd personal-finance-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your_key" > .env
streamlit run app.py
```

## 📂 Project Structure

```
personal-finance-tracker/
├── src/
│   ├── processor.py     # CSV loading, summary, category breakdown
│   ├── charts.py        # Plotly pie, bar, cashflow, waterfall charts
│   └── ai_insights.py  # Groq LLM financial insight generation
├── data/
│   └── sample_transactions.csv
├── app.py               # Streamlit dashboard
├── requirements.txt
├── .gitignore
└── README.md
```

## What I Learned

- How to process and aggregate financial data with pandas
- How to build a waterfall chart with Plotly Graph Objects
- How to inject real data into LLM prompts for specific, grounded insights
- How to handle multiple data sources (CSV upload vs sample) in Streamlit
- How to use st.session_state and sidebar controls cleanly

## 🚀 Let's Connect!
I am actively writing clean code and sharing my growth architecture openly with the community.

Follow my progress: [GitHub Profile](https://github.com/iamxkhushi1726-svg)
