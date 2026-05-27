import streamlit as st
import pandas as pd

from services.google_trends import get_google_trends
from services.rss_news import get_news
from services.deepseek_ai import analyze_trends

st.set_page_config(
    page_title="Indonesia Trend Intelligence",
    layout="wide"
)

# =========================
# LOAD SECRET API KEY
# =========================
api_key = st.secrets["DEEPSEEK_API_KEY"]

st.title("🇮🇩 Indonesia Trend Intelligence")

st.markdown("""
AI Dashboard untuk:
- Google Trends Indonesia
- Viral News Indonesia
- Analisa AI DeepSeek
""")

# =========================
# AUTO LOAD DATA
# =========================
with st.spinner("Mengambil data terbaru..."):

    # =========================
    # GOOGLE TRENDS
    # =========================
    try:
        trends = get_google_trends()

    except Exception as e:
        trends = [f"Error Google Trends: {e}"]

    # =========================
    # RSS NEWS
    # =========================
    try:
        news = get_news()

    except Exception as e:
        news = [f"Error News: {e}"]

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
        ai_result = f"Error AI: {e}"

# =========================
# DISPLAY AI RESULT
# =========================
st.subheader("🔥 AI Trend Analysis")

st.markdown(ai_result)

# =========================
# DISPLAY TABLES
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
# CHART
# =========================
st.subheader("📊 Trend Ranking")

chart_df = pd.DataFrame({
    "keyword": trends[:10],
    "score": list(range(10, 0, -1))
})

chart_df = chart_df.set_index(
    "keyword"
)

st.bar_chart(chart_df)
