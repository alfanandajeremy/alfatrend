import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit_option_menu import option_menu

from services.google_trends import get_google_trends
from services.rss_news import get_news
from services.deepseek_ai import analyze_trends

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Trend Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# LOAD CSS
# =========================
def load_css():

    with open("assets/style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    selected = option_menu(
        menu_title="Dashboard",
        options=[
            "Overview",
            "Trending",
            "News",
            "AI Analysis"
        ],
        icons=[
            "house",
            "graph-up",
            "newspaper",
            "robot"
        ],
        default_index=0
    )

# =========================
# SECRET API KEY
# =========================
api_key = st.secrets["DEEPSEEK_API_KEY"]

# =========================
# GET DATA
# =========================
try:
    trends = get_google_trends()

    if not isinstance(trends, list):
        trends = list(trends)

except Exception as e:

    trends = [
        f"Google Trends Error: {e}"
    ]

try:
    news = get_news()

except Exception as e:

    news = [
        f"News Error: {e}"
    ]

# =========================
# COMBINE DATA
# =========================
combined_text = "\n".join(
    trends + news
)

# =========================
# AI ANALYSIS
# =========================
try:

    ai_result = analyze_trends(
        api_key,
        combined_text
    )

except Exception as e:

    ai_result = f"AI Error: {e}"

# =========================
# HEADER
# =========================
st.markdown("""
<div class="main-title">
INDONESIA TREND INTELLIGENCE
</div>
""", unsafe_allow_html=True)

# =========================
# METRIC CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown("""
    <div class="metric-card">
        <h2>24</h2>
        <p>Trending Topics</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="metric-card">
        <h2>89%</h2>
        <p>Positive Sentiment</p>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="metric-card">
        <h2>120K</h2>
        <p>Total Mentions</p>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="metric-card">
        <h2>18</h2>
        <p>Emerging Trends</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# TREND CHART
# =========================
st.subheader("📈 Trending Chart")

# FIX LENGTH ISSUE
trend_count = min(len(trends), 10)

chart_df = pd.DataFrame({
    "keyword": trends[:trend_count],
    "score": list(range(trend_count, 0, -1))
})

if not chart_df.empty:

    fig = px.line(
        chart_df,
        x="keyword",
        y="score",
        markers=True
    )

    fig.update_layout(
        paper_bgcolor="#0d0221",
        plot_bgcolor="#0d0221",
        font_color="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning("No trend data available")

# =========================
# TABLES
# =========================
col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Google Trends")

    trend_df = pd.DataFrame({
        "Trending Keyword": trends
    })

    st.dataframe(
        trend_df,
        use_container_width=True
    )

with col2:

    st.subheader("📰 News Headlines")

    news_df = pd.DataFrame({
        "Headline": news
    })

    st.dataframe(
        news_df,
        use_container_width=True
    )

# =========================
# AI RESULT
# =========================
st.subheader("🤖 AI Trend Analysis")

st.markdown(f"""
<div class="ai-box">
{ai_result}
</div>
""", unsafe_allow_html=True)
