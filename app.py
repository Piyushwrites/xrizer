# ========================
# XRIZER PERMANENT WEB APP - DAY 1.5 (Professional Version)
# ========================

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

st.set_page_config(page_title="Xrizer", page_icon="🚀", layout="centered")

st.title("🚀 Xrizer")
st.caption("AI Meeting & Video Summarizer — Built by Piyush ❤️")

# Secure key input (never saved)
gemini_key = st.text_input("🔑 Enter your Gemini API Key", type="password", 
                          help="Only used for this session. Safe & private.")

if not gemini_key:
    st.warning("👆 Paste your Gemini API key above to start using Xrizer.")
    st.stop()

genai.configure(api_key=gemini_key)
model = genai.GenerativeModel("gemini-2.5-flash")

st.success("✅ Xrizer is ready!")

tab1, tab2 = st.tabs(["📝 Paste Text / Meeting Notes", "🎥 YouTube Video"])

with tab1:
    text = st.text_area("Paste your meeting notes or transcript here...", height=220)
    if st.button("✨ Generate Summary", type="primary", use_container_width=True):
        with st.spinner("Xrizer is thinking..."):
            prompt = f"""You are Xrizer — the world's best AI meeting & video summarizer.

Return ONLY in this exact format:

**📋 Executive Summary**
- Bullet 1
- Bullet 2
- Bullet 3

**🔑 Key Decisions** (if any)

**✅ Action Items**
• Person → Task → Deadline

**💡 Follow-up Suggestions** (1-2 smart ideas)

Text:
{text}"""

            response = model.generate_content(prompt)
            st.success("✅ Summary Ready!")
            st.markdown(response.text)
            
            st.download_button("📥 Download as Markdown", 
                             response.text, 
                             file_name="Xrizer_Summary.md",
                             mime="text/markdown")

with tab2:
    yt_link = st.text_input("Paste YouTube link", placeholder="https://www.youtube.com/watch?v=...")
    if st.button("🎥 Summarize YouTube Video", type="primary", use_container_width=True):
        with st.spinner("Fetching transcript..."):
            try:
                if "v=" in yt_link:
                    video_id = yt_link.split("v=")[1].split("&")[0]
                else:
                    video_id = yt_link.split("/")[-1]
                
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([item['text'] for item in transcript])
                
                response = model.generate_content(f"""You are Xrizer. Summarize this video in the exact format above.

Transcript: {full_text[:15000]}""")
                
                st.success("✅ Video Summary Ready!")
                st.markdown(response.text)
                st.download_button("📥 Download Video Summary", 
                                 response.text, 
                                 file_name="Xrizer_YouTube_Summary.md",
                                 mime="text/markdown")
            except:
                st.error("Transcript not available. Try another public YouTube video.")

st.caption("Made with ❤️ by Piyush | Project Xrizer | 70+hour dedication 🔥")
