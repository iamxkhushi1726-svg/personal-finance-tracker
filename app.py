import sys
import os
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.processor import (
    load_transactions,
    compute_summary,
    get_category_breakdown,
    get_daily_cashflow,
)
from src.charts import (
    pie_chart_expenses,
    bar_chart_categories,
    line_chart_cashflow,
    waterfall_chart,
)
from src.ai_insights import generate_insights

# ── PAGE CONFIGURATION ──────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise Financial Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# ── IMMUTABLE LIGHT THEME CSS INJECTION ─────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,100..900;1,100..900&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

    /* BASE STRUCTURAL THEME IMMUTABILITY */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #FFFDF9 !important;
        background: #FFFDF9 !important;
    }
    
    /* WARM CREAM NAVIGATION LAYER */
    [data-testid="stSidebar"] {
        background-color: #FFF9F1 !important;
        border-right: 1px solid #FFE5BF !important;
    }
    
    /* REFINED SAAS ELEMENTS & LABELS */
    .stMarkdown p, .stCaption, label, [data-testid="stWidgetLabel"] p, .stSelectbox div {
        font-family: 'Noto Serif', serif !important;
        color: #2D2522 !important;
    }
    
    /* HEADERS & BRAND DISPLAY */
    h1, h2, h3, h4, h5, h6, [data-testid="stMetricLabel"] p, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        color: #1E120E !important;
    }

    /* PREMIUM METRIC CARDS INTEGRATION */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FFE5BF !important;
        border-radius: 12px !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(230, 28, 56, 0.02) !important;
    }

    [data-testid="stMetricValue"] div {
        font-family: 'Playfair Display', serif !important;
        font-weight: 800 !important;
        color: #E61C38 !important;
    }
    
    /* PREMIUM STRUCTURAL CONTAINER FOR AI INSIGHTS */
    .ai-insight-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #FFFDF9 100%) !important;
        border-left: 5px solid #E61C38 !important;
        border-top: 1px solid #FFE5BF !important;
        border-right: 1px solid #FFE5BF !important;
        border-bottom: 1px solid #FFE5BF !important;
        border-radius: 4px 12px 12px 4px !important;
        padding: 2rem !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 6px 18px rgba(30, 18, 14, 0.03) !important;
    }
    
    .ai-insight-card h4 {
        margin-top: 0 !important;
        color: #E61C38 !important;
        font-size: 1.25rem !important;
        letter-spacing: 0.5px !important;
    }

    /* LAYOUT COMPONENT FRAMES */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1E120E !important;
        border: 1px solid #FFE5BF !important;
        border-radius: 6px !important;
    }
    
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FFE5BF !important;
        border-radius: 8px !important;
    }

    /* SIGNATURE CRIMSON CALL TO ACTION BUTTON */
    div.stButton > button:first-child {
        background-color: #E61C38 !important;
        color: #FFFFFF !important;
        border: 1px solid #E61C38 !important;
        border-radius: 6px !important;
        font-family: 'Noto Serif', serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #B51227 !important;
        border-color: #B51227 !important;
    }

    /* COMPONENT SEGMENT MARGINS */
    hr {
        border-top: 1px solid #FFE5BF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── DASHBOARD HEADER ────────────────────────────────────────────
st.title("Financial Analytics & Intelligence Platform")
st.markdown(
    """
    Welcome to your central financial intelligence command center. This platform 
    aggregates multi-channel transactional data, yields interactive cash flow visualizations, 
    and leverages advanced language models to deliver automated financial insights.
    """
)
st.markdown("---")

# ── PREMIUM SIDEBAR CONTROL PANEL ───────────────────────────────
st.sidebar.title("Data Management")
st.sidebar.caption("System Data Source Configuration")
st.sidebar.markdown(" ")

data_source = st.sidebar.radio(
    "Select Ingestion Protocol",
    ["Upload Production CSV", "Generate Demo Dataset"],
    help="Choose whether to stream your own transaction ledger or explore the platform's capabilities using synthetic financial data.",
)

st.sidebar.markdown("---")

df = pd.DataFrame()

if data_source == "Upload Production CSV":
    st.sidebar.subheader("File Ingestion Inbound")
    uploaded = st.sidebar.file_uploader(
        "Drop file or click to browse",
        type=["csv"],
        help="The ingestion engine expects a standard comma-separated ledger mapping historical transactional records.",
    )
    if uploaded:
        with st.spinner("Parsing data stream..."):
            df, err = load_transactions(uploaded)
        if err:
            st.sidebar.error(f"Ingestion Failure: {err}")
            st.stop()
        st.sidebar.success("Data pipeline established successfully.")
else:
    df, err = load_transactions("data/sample_transactions.csv")
    if err:
        st.sidebar.error(f"Demo Data Load Failure: {err}")
        st.stop()
    st.sidebar.info(
        "Standard sandbox active. Toggle above to upload custom organizational sheets."
    )

st.sidebar.markdown("---")
st.sidebar.subheader("Required Schema Definition")
st.sidebar.caption("Source arrays must fully correspond to the structure below:")
st.sidebar.code(
    "date,description,category,amount,type\n2026-05-01,Salary,Income,45000,income\n2026-05-02,Vendor,Food,450,expense",
    language="text",
)

# ── INITIAL DATA VALIDATION GUARD ───────────────────────────────
if df.empty:
    st.info(
        "System Ready: Awaiting data ingestion. Please utilize the sidebar control panel to upload your transaction history or select the demo pipeline."
    )
    st.stop()

# ── CORE DATA ARCHITECTURE ──────────────────────────────────────
summary = compute_summary(df)
breakdown = get_category_breakdown(df)
daily = get_daily_cashflow(df)

# ── SECTION 1: EXECUTIVE KEY PERFORMANCE INDICATORS ─────────────
st.header("Executive Financial Summary")
st.markdown(
    "A macro-level breakdown of core liquidity metrics, operational burn rates, and transaction velocity."
)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(
    label="Gross Inflow", 
    value=f"₹{summary['total_income']:,.0f}"
)
col2.metric(
    label="Gross Outflow", 
    value=f"₹{summary['total_expense']:,.0f}"
)
savings_delta = f"↑ {summary['savings_rate']}% Net Retention"
col3.metric(
    label="Net Capital Retention", 
    value=f"₹{summary['net_savings']:,.0f}", 
    delta=savings_delta
)
col4.metric(
    label="Primary Cost Center", 
    value=summary["top_category"], 
    delta=f"↑ ₹{summary['top_category_amt']:,.0f} Vol"
)
col5.metric(
    label="Audited Records", 
    value=summary["num_transactions"], 
    delta=f"↑ {summary['date_range']}", 
    delta_color="off"
)

st.markdown("---")

# ── SECTION 2: ALLOCATION & CATEGORICAL VISUALIZATIONS ─────────
st.header("Expenditure Architecture & Capital Allocation")
st.markdown(
    "Granular breakdowns analyzing structural cost distribution across operational categories."
)

col_left, col_right = st.columns(2)
with col_left:
    st.plotly_chart(pie_chart_expenses(breakdown), use_container_width=True)
    st.caption(
        "**Proportional Capital Contribution:** Represents relative weight allocations per expense vertical."
    )
with col_right:
    st.plotly_chart(bar_chart_categories(breakdown), use_container_width=True)
    st.caption(
        "**Categorical Velocity:** Absolute spending volume charted linearly by organizational segment."
    )

st.markdown("---")

# ── SECTION 3: LIQUIDITY VELOCITY & TREASURY FLOWS ──────────────
st.header("Liquidity Velocity & Cash Flow Dynamics")
st.markdown(
    "Time-series monitoring charting daily runway movements alongside net cumulative changes."
)

st.plotly_chart(line_chart_cashflow(daily), use_container_width=True)
st.caption(
    "**Daily Treasury Tracking:** Chronological trendlines highlighting cash positioning over the reporting window."
)

st.plotly_chart(waterfall_chart(summary), use_container_width=True)
st.caption(
    "**Capital Reconciliation Waterfall:** Bridge breakdown illustrating inflows pacing down into distinct liabilities and remaining net position."
)

st.markdown("---")

# ── SECTION 4: DEEP INSIGHT ENGINE (AI CORE) ─────────────────────
st.header("Automated Institutional Intelligence")
st.markdown(
    "Generate on-demand analytical narratives outlining capital optimization strategies and behavioral spending alerts."
)

with st.container():
    if st.button("Execute Automated Financial Audit", type="primary"):
        with st.spinner("Processing transaction matrix via Llama-3 Engine..."):
            insights = generate_insights(summary, breakdown)
        
        st.markdown(
            f"""
            <div class="ai-insight-card">
                <h4>EXECUTIVE ANALYTICAL SYNTHESIS</h4>
                <div style="line-height: 1.6; font-size: 0.95rem; font-family: 'Noto Serif', serif;">
                    {insights}
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.caption(
            "Clicking the optimizer above will run the matrix calculations against the AI narrative generation engine."
        )

st.markdown("---")

# ── SECTION 5: AUDITED TRANSACTIONAL REGISTRY ──────────────────
st.header("Indexed Ledger Registry")
st.markdown(
    "An un-pivoted, filterable look at complete operational records underlying the aggregate charts."
)

col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    categories = ["All Frameworks"] + sorted(df["category"].unique().tolist())
    selected_cat = st.selectbox("Isolate Category", categories)
with col_filter2:
    types = ["All Directions", "income", "expense"]
    selected_type = st.selectbox("Isolate Ledger Direction", types)

filtered_df = df.copy()
if selected_cat != "All Frameworks":
    filtered_df = filtered_df[filtered_df["category"] == selected_cat]
if selected_type != "All Directions":
    filtered_df = filtered_df[filtered_df["type"] == selected_type]

st.dataframe(
    filtered_df[["date", "description", "category", "amount", "type"]]
    .sort_values("date", ascending=False),
    use_container_width=True,
)

# ── FOOTER ──────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "CONFIDENTIALITY NOTICE: This dashboard functions completely as a client-side visualization layer. All transaction metrics remain local to your memory ecosystem."
)