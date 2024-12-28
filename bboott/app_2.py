import streamlit as st
from google.cloud import aiplatform
import pdfplumber
import google.generativeai as genai
import os
from PIL import Image

# Set the environment variable
genai.configure(api_key="AIzaSyDij2IXvrnk442HYg5g1rRkb_672lJ0cZI")

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Function to get a summary from Gemini-pro API
def summarize_text(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please summarize the following text:\n\n{text}"])  # Increase timeout
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Function to question text using Gemini-pro API
def question_text(text, question):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([f"Please answer the following question based on the provided text:\n\nText: {text}\n\nQuestion: {question}"])  # Increase timeout
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app
def main():
    st.title("Multiple PDF Summarizer and Question Answering with AI")
    
    image = Image.open('bytebuddies.jpg')
    st.image(image, use_container_width='always')
    
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        all_texts = {}

        for uploaded_file in uploaded_files:
            # Extract text from the uploaded PDF
            text = extract_text_from_pdf(uploaded_file)
            all_texts[uploaded_file.name] = text

        # Display extracted text for each file
        for file_name, text in all_texts.items():
            st.subheader(f"Extracted Text from {file_name}")
            display_text = text[:500] + ('...' if len(text) > 500 else '')
            st.text_area(f"Text from {file_name}", display_text, height=300)

        # Get a summary for each file
        if st.button("Get Summaries"):
            for file_name, text in all_texts.items():
                summary = summarize_text(text)
                st.subheader(f"Summary for {file_name}")
                st.write(summary)

        # Ask a question about all files
        question = st.text_input("Enter your question about the texts")
        if st.button("Get Answers"):
            if question:
                for file_name, text in all_texts.items():
                    answer = question_text(text, question)
                    st.subheader(f"Answer for {file_name}")
                    st.write(answer)
            else:
                st.warning("Please enter a question to get an answer.")

if __name__ == "__main__":
    main()
