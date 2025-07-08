import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini
prompt = "Please summarize this video transcript into 250 words or less, highlighting key points:\n\n"

# Function to extract transcript from YouTube
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([t["text"] for t in transcript_text])
        return transcript
    except Exception as e:
        return f"Error fetching transcript: {e}"

# Function to summarize using Google Gemini
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")
st.title("🎬 YouTube Video Summarizer using Gemini AI")

youtube_link = st.text_input("Enter YouTube Video URL")

if st.button("Get Detailed Notes"):
    with st.spinner("⏳ Processing... Please wait"):
        transcript = extract_transcript_details(youtube_link)
        if transcript.startswith("Error"):
            st.error(transcript)
        else:
            summary = generate_gemini_content(transcript, prompt)
            st.markdown("### 📌 Detailed Summary:")
            st.write(summary)
