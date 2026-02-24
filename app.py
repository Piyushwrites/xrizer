import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# ────────────────────────────────────────────────
# Server-side Gemini Key (Hidden & Secure)
# ────────────────────────────────────────────────
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ────────────────────────────────────────────────
# Visual Polish (already added earlier)
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="Xrizer – AI Meeting & Video Summarizer",
    page_icon="🚀",
    layout="centered"
)

# Custom CSS (keep your previous CSS if you added it)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 800px !important; }
    h1 { text-align: center; font-size: 2.5rem !important; margin-bottom: 0.5rem !important; }
    .stCaption { text-align: center; color: #9ca3af !important; font-size: 0.95rem !important; }
    .stButton > button { width: 100%; height: 3rem; font-weight: 600; border-radius: 0.5rem; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Xrizer")
st.caption("AI Meeting & Video Summarizer — Built by Piyush ❤️")

# ←←← ONLY ONE SUCCESS MESSAGE HERE ←←←
st.success("✅ Xrizer is ready!")

tab1, tab2 = st.tabs(["📝 Paste Text / Meeting Notes", "🎥 YouTube Video"])

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
