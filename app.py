# ========================
# XRIZER PERMANENT WEB APP - DAY 1.5 (Professional Version)
# ========================

import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
# Custom CSS for premium polish
st.markdown("""
    <style>
        /* Better spacing & centering */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 800px !important;  /* Keeps it centered on wide screens */
        }
        
        /* Title styling - bigger, bolder */
        h1 {
            text-align: center;
            font-size: 2.5rem !important;
            margin-bottom: 0.5rem !important;
            color: #ffffff;  /* White for contrast in dark mode */
        }
        
        /* Caption - subtle & centered */
        .stCaption {
            text-align: center;
            color: #9ca3af !important;  /* Soft gray */
            font-size: 0.95rem !important;
        }
        
        /* Buttons - premium feel with hover animation */
        .stButton > button {
            width: 100%;
            height: 3rem;
            font-weight: 600;
            border-radius: 0.5rem;
            background-color: #3b82f6;  /* Blue for primary action */
            color: white;
            border: none;
            transition: all 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);  /* Subtle blue glow */
        }
        
        /* Inputs - clean borders & focus */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 0.5rem;
            border: 1px solid #4b5563;  /* Soft gray border */
            background-color: #1f2937;  /* Darker input bg */
            color: white;
        }
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3b82f6;  /* Blue focus ring */
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
        }
        
        /* Success/alert boxes - rounded */
        .stSuccess, .stWarning, .stError, .stInfo {
            border-radius: 0.5rem;
            padding: 1rem !important;
        }
        
        /* Mobile responsiveness - ensure no overflow */
        @media (max-width: 640px) {
            .block-container { padding-left: 1rem !important; padding-right: 1rem !important; }
            h1 { font-size: 2rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Xrizer – AI Meeting & Video Summarizer",
    page_icon="https://i.imgur.com/0k7jX0C.png",  # Temporary free icon - replace with your own
    layout="centered"
)

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
