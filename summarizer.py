import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import streamlit as st

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load('en_core_web_sm')

def summarize_text(text, num_sentences=3):
    # Process the text with spaCy
    doc = nlp(text)
    
    # Calculate word frequencies excluding stop words
    word_freq = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS:
            if word.text.lower() not in word_freq:
                word_freq[word.text.lower()] = 1
            else:
                word_freq[word.text.lower()] += 1
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sent in doc.sents:
        score = 0
        for word in sent:
            if word.text.lower() in word_freq:
                score += word_freq[word.text.lower()]
        sentence_scores[sent] = score
    
    # Select top sentences based on scores
    summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summarized_text = ' '.join([sent.text for sent in summarized_sentences])
    
    return summarized_text

def main():
    # Set page title and header with colors
    st.title("Text Summarizer")
    st.markdown(
        """
        <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #00dc00; /* Dark cyan */
            padding: 10px;
            background-color: #dccf00; /* Light gray */
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .subheader {
            font-size: 24px;
            color: #00d2dc; /* Dark gray */
            margin-top: 20px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Header for input section
    st.markdown("<h2 class='subheader'>Enter your text below:</h2>", unsafe_allow_html=True)
    
    # Input text area with custom styling
    text = st.text_area("Input text", height=200, key='input_textarea')
    st.markdown(
        """
        <style>
        .input_textarea {
            font-size: 16px;
            padding: 10px;
            border: 2px solid #008080; /* Dark cyan */
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Summarize button
    if st.button("Summarize"):
        if text.strip():  # Check if input text is not empty
            summary = summarize_text(text)
            st.markdown("---")
            st.markdown("<h2 class='subheader'>Summarized Text:</h2>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color:##dc0017; padding:10px; border-radius:10px;'>{summary}</div>", unsafe_allow_html=True)
        else:
            st.warning("Please enter some text to summarize.")  # Warn if no text entered

if __name__ == "__main__":
    main()
