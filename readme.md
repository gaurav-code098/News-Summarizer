<h1 text align = center >
🗞️ News Article Summarizer
</h1>
<p1> This is a  Streamlit app  that allows users to summarize news articles either by pasting raw text or providing a news <b>URL</b>. It uses a <b> pre-trained NLP model </b> for summarization and also displays trending news from <b> Multiple Trusted Sources </b> .</p1>
<h2>
   🧠Model 
</h2>
<p>This project uses a pre-trained model from <b> Hugging Face Transformers<b>, a popular open-source library for <b> Natural Language Processing</b>.</p>
<p> Summarization using the  model (sshleifer/distilbart-cnn-12-6) from Hugging Face Transformers <br> </p>

<h2>
   🚀 Features
</h2>
<p>
- Paste raw Text or a News URL to get a summary. <br>
- Click on trending headlines to auto-summarize them. <br>
- Trending headlines are fetched from RSS feeds with multiple source <br>
- Clean and minimal UI.<br>
- Trending News sources - <b>BCC World, CNN World, India Today, The Hindu, Indian Express,  NDTV</b> etc

</p>
<h2>
🛠 Set-up <br>
   </h2>
<p>
git clone https://github.com/yourusername/news-summarizer.git<br>
cd news-summarizer<br>
pip install -r requirements.txt <br>
streamlit run main.py
</p>
