import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import re

from streamlit_option_menu import option_menu

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
            "News",
            "AI Analysis"
        ],
        icons=[
            "house",
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
# GET NEWS
# =========================
try:

    news = get_news()

except Exception as e:

    news = [
        f"News Error: {e}"
    ]

# =========================
# COMBINE TEXT
# =========================
combined_text = "\n".join(news)

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
# KEYWORD EXTRACTION
# =========================
all_text = " ".join(news).lower()

words = re.findall(
    r'\b[a-zA-Z]{4,}\b',
    all_text
)

stopwords = {
    "yang",
    "dari",
    "untuk",
    "dengan",
    "karena",
    "dalam",
    "pada",
    "adalah",
    "setelah",
    "hingga",
    "tentang"
}

filtered_words = [
    word for word in words
    if word not in stopwords
]

word_freq = Counter(
    filtered_words
)

top_keywords = word_freq.most_common(10)

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

    st.markdown(f"""
    <div class="metric-card">
        <h2>{len(news)}</h2>
        <p>Total Headlines</p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="metric-card">
        <h2>AI</h2>
        <p>Trend Analysis</p>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <h2>{len(top_keywords)}</h2>
        <p>Top Keywords</p>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown("""
    <div class="metric-card">
        <h2>LIVE</h2>
        <p>News Monitoring</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# TREND CHART
# =========================
st.subheader("📈 Trending Keywords")

if top_keywords:

    chart_df = pd.DataFrame(
        top_keywords,
        columns=[
            "keyword",
            "count"
        ]
    )

    fig = px.bar(
        chart_df,
        x="keyword",
        y="count",
        color="count"
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

    st.warning(
        "No keyword data"
    )

# =========================
# NEWS TABLE
# =========================
st.subheader("📰 News Headlines")

news_df = pd.DataFrame({
    "Headline": news
})

st.dataframe(
    news_df,
    use_container_width=True
)

# =========================
# AI ANALYSIS
# =========================
st.subheader("🤖 AI Trend Analysis")

st.markdown(f"""
<div class="ai-box">
{ai_result}
</div>
""", unsafe_allow_html=True)
