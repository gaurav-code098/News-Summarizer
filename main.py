import streamlit as st
from utils import extract_text_from_url
# Import the NEW functions and the RSS_FEEDS dict
from fetch_news import fetch_breaking_news, fetch_general_news, RSS_FEEDS
from summarizer import summarize_text , load_qa_pipeline , answer_question
from urllib.parse import urlparse
from ddgs import DDGS
from typing import List, Dict
import json

st.set_page_config(page_title="📰 News Article Summarizer")
st.markdown('<h1 style="text-align: center;">📰 News Article Summarizer</h1>', unsafe_allow_html=True)


# --- Summarization from URL or Raw Text (This section is unchanged) ---
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

# --- Helper Function to Display Articles (NEW) ---
# This avoids repeating code in our tabs!
def display_articles(articles: list, key_prefix: str):
    
    if not articles:
        st.info("No articles found for this source.")
        return

    for idx, article in enumerate(articles):
        with st.expander(f"{article['title']} ({article['published']})"):
            st.markdown(article['summary'], unsafe_allow_html=True)
            st.markdown(f"[🔗 Full Article]({article['link']})")
            
            # We use the key_prefix and index to make a unique key
            if st.button(f"Summarize This Article", key=f"summarize_{key_prefix}_{idx}"):
                
                # Use the article link to get the full text
                text_to_summarize = article.get('link')
                
                if text_to_summarIZE:
                    with st.spinner("Summarizing..."):
                        full_text = extract_text_from_url(text_to_summarize)
                        
                        if full_text:
                            summary_result = summarize_text(full_text)
                            st.success("Summary:")
                            st.markdown(f"""
                            <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                                {summary_result}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Could not extract text from the article link.")
                else:
                    st.warning("No article link available to summarize.")

TRUSTED_DOMAINS = [
    "indiatoday.in",
    "indianexpress.com",
    "ndtv.com",
    "thehindu.com",
    "timesofindia.com",
    "hindustantimes.com",
    "newsbytesapp.com",
    "techcrunch.com",
    "nytimes.com",
    "theguardian.com",
]

# --- REFACTORED RSS Trending News Section (Using Tabs) ---
st.subheader("📰 Trending Articles")

tab1, tab2, tab3 , tab4,tab5 = st.tabs(["⚡ Breaking News", "📰 General News", "💻 Tech News" , "🌐Around TheWorld" , "🤖Ask AI"])

with tab1:
    # 1. Call the 5-minute cache function
    breaking_articles = fetch_breaking_news(RSS_FEEDS["NDTV"])
    # 2. Use the helper to display them (FIXED: Removed typo from your code)
    display_articles(breaking_articles, key_prefix="breaking")

with tab2:
    # 1. Call the 30-minute cache function
    general_articles = fetch_general_news(RSS_FEEDS["Times of India"])
    # 2. Use the helper to display them
    display_articles(general_articles, key_prefix="general")

with tab3:
    # 1. Call the 30-minute cache function (it's reusable!)
    tech_articles = fetch_general_news(RSS_FEEDS["TechCrunch"])
    # 2. Use the helper to display them
    display_articles(tech_articles, key_prefix="tech")

with tab4:
    # 1. Call the 30-minute cache function (it's reusable!)
    Around_world = fetch_general_news(RSS_FEEDS["BBC World"])
    # 2. Use the helper to display them
    display_articles(Around_world, key_prefix="World")

with tab5:
    st.subheader("Ask About Anything")
    st.markdown("I will search trusted news sites or our RSS feeds to find an answer.")
    
    question = st.text_input("Ask your question:", 
                             placeholder="e.g., Ask Questions regarding Today's news!")

    if st.button("Get Answer", key="qa_button"):
        if not question:
            st.warning("Please ask a question.")
        else:
            clean_question = question.lower().strip()
            
            # --- 1. THE "SUPER ROUTER" (for Tech) ---
            if "tech" in clean_question or "technology" in clean_question:
                
                st.info("Tech question detected! Fetching from internal TechCrunch RSS feed...")
                with st.spinner("Fetching TechCrunch news..."):
                    tech_articles = fetch_general_news(RSS_FEEDS["TechCrunch"])
                    
                    if not tech_articles:
                        st.error("Could not fetch articles from TechCrunch RSS feed.")
                        st.stop()
                    
                    all_summaries = [article['summary'] for article in tech_articles]
                    context = " ".join(all_summaries)

                with st.spinner("Summarizing tech news..."):
                    answer = summarize_text(context)
                    st.subheader("Summary of What's Happening in Tech:")
                    st.markdown(f"""
                    <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                        {answer}
                    </div>
                    """, unsafe_allow_html=True)
            
            else:
                # --- 2. THE "ELSE" BLOCK (for all other questions) ---
                
                context = ""
                with st.spinner(f"Searching trusted sites for: '{question}'..."):
                    
                    site_query = " OR ".join([f"site:{domain}" for domain in TRUSTED_DOMAINS])
                    final_query = f"{question} ({site_query})"
                    
                    try:
                        search_results: List[Dict[str, str]] = DDGS().text(
                            query=final_query,
                            region="in-en",
                            max_results=5,
                            timelimit="w"
                        )
                        
                        if not search_results:
                            st.error("No results found on your trusted news sites for that query.")
                            st.stop()

                        print("--- RAW SEARCH RESULTS (DEBUG) ---")
                        print(json.dumps(search_results, indent=2))
                        print("---------------------------------")

                    except Exception as e:
                        st.error(f"Error searching DuckDuckGo: {e}")
                        st.stop()
                
                with st.spinner("Reading search summaries..."):
                    all_summaries = []
                    for result in search_results[:5]: # Use top 5
                        if "body" in result:
                            all_summaries.append(result["body"])

                    context = " ".join(all_summaries)
                    
                    if not context:
                        st.error("I found results, but they had no text summaries.")
                        st.stop()

                # --- 4. THE "SMART ROUTER" (Long/Short Answer) ---
                with st.spinner("Analyzing and generating answers..."):
                    
                    broad_question_triggers = ("what's happening", "what's new", "tell me about", "summarize")
                    
                    if any(clean_question.startswith(trigger) for trigger in broad_question_triggers):
                        # --- BROAD QUESTION ---
                        st.write("Broad question detected. Running Summarizer...")
                        answer = summarize_text(context)
                        
                        # --- FIX: Create an HTML link ---
                        first_result_url = search_results[0].get('href', '#')
                        html_link = f'<a href="{first_result_url}" target="_blank" style="color: #00BFFF; text-decoration: none;">🔗 Read the top article</a>'
                        answer_with_link = f"{answer}<br><br>{html_link}"
                        
                        st.subheader("Summary of Findings:")
                        st.markdown(f"""
                        <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                            {answer_with_link}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    else:
                        # --- SPECIFIC QUESTION ---
                        st.write("Specific question detected. Running QA and Summarizer...")
                        
                        short_answer = answer_question(question, context)
                        long_answer = summarize_text(context)
                        
                        # --- FIX: Create an HTML link ---
                        first_result_url = search_results[0].get('href', '#')
                        html_link = f'<a href="{first_result_url}" target="_blank" style="color: #00BFFF; text-decoration: none;">🔗 Read the top article</a>'
                        long_answer_with_link = f"{long_answer}<br><br>{html_link}"
                        
                        is_too_short = len(short_answer.split()) < 4
                        quick_answer_display = ""
                        
                        if is_too_short:
                            st.write("QA answer is too short. Using first sentence of summary instead.")
                            try:
                                quick_answer_display = long_answer.split('.')[0] + '.'
                            except Exception:
                                quick_answer_display = long_answer
                        else:
                            quick_answer_display = short_answer
                        
                        st.subheader("Quick Answer:")
                        st.markdown(f"""
                        <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                            {quick_answer_display}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.subheader("Detailed Summary:")
                        st.markdown(f"""
                        <div style='background-color:#202020; padding: 1rem; border-radius: 12px; color: white'>
                            {long_answer_with_link}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    # --- "Show raw search results" expander is removed ---
