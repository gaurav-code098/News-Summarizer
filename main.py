import streamlit as st
from fetch_news import get_articles, RSS_FEEDS
from summarizer import summarize_text
from utils import extract_text_from_url

st.set_page_config(page_title="📰  News Article Summarizer")
st.markdown('<h1 style="text-align: center;">📰 News Article Summarizer</h1>', unsafe_allow_html=True)


# --- Summarization from URL or Raw Text ---
st.subheader("🔗 Summarize from URL or Raw Text")
user_input = st.text_area("Paste article URL or raw text")

if st.button("Summarize"):
    if user_input.startswith("http"):
        text = extract_text_from_url(user_input)
    else:
        text = user_input
    if text:
        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
            st.success("Summary:")
            st.markdown(f"""
            <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                {summary}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Failed to extract or process the text.")

# --- RSS Trending News Section ---
st.subheader("📰 Trending Articles ")
source = st.selectbox("Choose Source", list(RSS_FEEDS.keys()))
articles = get_articles(RSS_FEEDS[source])

for idx, article in enumerate(articles):
    with st.expander(f"{article['title']} ({article['published']})"):
        st.markdown(article['summary'], unsafe_allow_html=True)
        if st.button(f"Summarize This Article {idx+1}"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(article['summary'])
                st.success("Summary:")
                st.write(summary)
            st.markdown(f"[🔗 Full Article]({article['link']})")
