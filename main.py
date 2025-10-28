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

# The key of the selectbox ensures its state is maintained correctly across reruns
articles = get_articles(RSS_FEEDS[source])

# Check if articles exist to prevent errors
if articles:
    for idx, article in enumerate(articles):
        # Use the article title and index to create a unique expander name
        with st.expander(f"{article['title']} ({article['published']})"):
            st.markdown(article['summary'], unsafe_allow_html=True)
            st.markdown(f"[🔗 Full Article]({article['link']})")
        
            if st.button(f"Summarize This Article", key=f"summarize_rss_{idx}"):
          
                text_to_summarize = article.get('link') or article['summary']
                with st.spinner("Summarizing..."):
                    # Use the URL to extract the full article text first (if it's a link)
                    if text_to_summarize.startswith("http"):
                        full_text = extract_text_from_url(text_to_summarize)
                    else:
                        # If the 'link' wasn't used, just use the RSS summary
                        full_text = text_to_summarize 
                    # Summarize the extracted text
                    summary_result = summarize_text(full_text)
                    st.success("Summary:")
                    # Display the newly generated summary
                    st.markdown(f"""
                    <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                        {summary_result}
                    </div>
                    """, unsafe_allow_html=True)
else:
    st.info(f"No articles found for the source: {source}")
