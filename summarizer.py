import streamlit as st
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# --- 1. NEW: Caching the Summarization Model ---
@st.cache_resource
def load_summarization_pipeline():
    """
    Loads the Hugging Face Summarization pipeline once and caches it.
    """
    # This is a standard, high-quality summarization model
    model_name = "sshleifer/distilbart-cnn-12-6" 
    print(f"--- LOADING SUMMARIZATION MODEL: {model_name} ---")
    summarizer = pipeline("summarization", model=model_name)
    return summarizer

# --- 2. UPGRADED: The summarize_text function ---
def summarize_text(text: str):
    """
    Summarizes the given text using the cached pipeline.
    We've added min_length and max_length for a longer summary.
    """
    # 1. Load the cached model
    summarizer = load_summarization_pipeline()
    
    # --- 3. THE KEY CHANGE: Set new length limits ---
    # You can adjust these numbers to whatever you like
    min_summary_length = 80  # Force it to be at least ~3-4 sentences
    max_summary_length = 200 # Allow it to be up to ~7-8 sentences
    
    try:
        summary = summarizer(
            text, 
            max_length=max_summary_length, 
            min_length=min_summary_length, 
            do_sample=False
        )
        return summary[0]['summary_text']
        
    except Exception as e:
        print(f"Error during summarization: {e}")
        # This is a common error if the source text is too short
        if "must be lower or equal to" in str(e):
             return "The source text is too short to summarize."
        return "Error: Could not generate summary."


# --- Question-Answering Functions (Unchanged) ---
@st.cache_resource
def load_qa_pipeline():
    """
    Loads the Hugging Face QA pipeline once and caches it.
    """
    model_name = "deepset/roberta-base-squad2"
    print(f"--- LOADING QA MODEL: {model_name} ---")
    qa_pipeline = pipeline(
        "question-answering",
        model=model_name,
        tokenizer=model_name
    )
    return qa_pipeline

def answer_question(question: str, context: str):
    """
    Answers a question given a context using the loaded model.
    """
    qa_pipeline = load_qa_pipeline()
    result = qa_pipeline(question=question, context=context)
    
    print(f"--- QA MODEL RESULT (DEBUG): ---")
    print(f"Answer: {result['answer']}")
    print(f"Score: {result['score']:.4f}") 
    
    if result['score'] < 0.05: 
        return f"(No confident answer found. Model score was {result['score']:.4f}). I'm not sure I can find that answer."
    else:
        return result['answer']