import streamlit as st
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer

# --- 1. NEW: Caching the Summarization Model ---
@st.cache_resource
def load_summarization_pipeline():
    """
    Loads the Hugging Face Summarization pipeline once and caches it.
    """
    # --- CHANGED: Using a much smaller, 6-layer model ---
    model_name = "sshleifer/distilbart-cnn-6-6" 
    print(f"--- LOADING SUMMARIZATION MODEL: {model_name} ---")
    summarizer = pipeline("summarization", model=model_name)
    return summarizer

# --- 2. UPGRADED: The summarize_text function ---
def summarize_text(text: str):
    """
    Summarizes the given text using the cached pipeline.
    """
    summarizer = load_summarization_pipeline()
    
    # --- CHANGED: Lowered min_length to work with the smaller model ---
    min_summary_length = 40  # Lowered from 80
    max_summary_length = 150 # Lowered from 200
    
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
        if "must be lower or equal to" in str(e):
             return "The source text is too short to summarize."
        return "Error: Could not generate summary."


# --- Question-Answering Functions ---
@st.cache_resource
def load_qa_pipeline():
    """
    Loads the Hugging Face QA pipeline once and caches it.
    """
    # --- CHANGED: Back to the small, fast 'distilbert' model ---
    model_name = "distilbert-base-cased-distilled-squad"
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
    
    # --- We'll keep the 0.05 threshold, this model works well ---
    if result['score'] < 0.05: 
        return f"(No confident answer found. Model score was {result['score']:.4f}). I'm not sure I can find that answer."
    else:
        return result['answer']