from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_model()

def summarize_text(text):
    if len(text.strip()) < 30:
        return "Text too short to summarize."
    try:
        summary = summarizer(text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Summarization failed: {e}"
