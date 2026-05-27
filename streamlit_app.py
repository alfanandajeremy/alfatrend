import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
# SECRET
# =========================
api_key = st.secrets["DEEPSEEK_API_KEY"]

# =========================
# LOAD DATA
# =========================
trends = get_google_trends()
news = get_news()

combined_text = "\n".join(
    trends + news
)

ai_result = analyze_trends(
    api_key,
    combined_text
)

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
# CHARTS
# =========================
chart_df = pd.DataFrame({
    "keyword": trends[:10],
    "score": list(range(10, 0, -1))
})

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

# =========================
# AI ANALYSIS
# =========================
st.markdown("""
<div class="section-title">
AI TREND ANALYSIS
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="ai-box">
{ai_result}
</div>
""", unsafe_allow_html=True)
