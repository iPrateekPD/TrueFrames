import streamlit as st
from backend.predict import scan_video
from PIL import Image
import os
import time

# ---------------------
# PAGE CONFIG
# ---------------------
st.set_page_config(
    page_title="Frames by DK - Deepfake Detection",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------
# CUSTOM CSS for Light Theme
# ---------------------
st.markdown("""
<style>
    /* Main background */
    .main {
        background-color: #ffffff;
        padding: 1rem;
    }

    /* Progress bar color */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }

    /* Result styles */
    .result-real {
        color: #2E7D32;
        font-weight: bold;
        font-size: 1.2em;
    }
    .result-fake {
        color: #C62828;
        font-weight: bold;
        font-size: 1.2em;
    }

    /* Alert box background colors */
    .stSuccess {
        background-color: #E8F5E9 !important;
    }
    .stError {
        background-color: #FFEBEE !important;
    }
    .stWarning {
        background-color: #FFF3E0 !important;
    }

    /* Frame images styling */
    .stImage img {
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------
# SIDEBAR
# ---------------------
st.sidebar.image("assets/logo.png", width=150)
st.sidebar.title("Frames by DK")
st.sidebar.markdown("**Team:** Desi Kalakaaar ❤️")
st.sidebar.markdown("---")
st.sidebar.markdown("📌 *Deepfake Video Detection powered by AI.*")
st.sidebar.markdown("🚀 Upload your video to detect manipulations.")
st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: For best results, upload videos under 50MB.")

# ---------------------
# HEADER SECTION
# ---------------------
col1, col2 = st.columns([1, 3])
with col1:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=120)
with col2:
    st.title("🎬 Frames by DK")
    st.subheader("AI-powered Deepfake Video Detection")
    with st.expander("ℹ About this project"):
        st.markdown("""
        **Frames by DK** scans videos frame-by-frame using AI to detect deepfakes.  
        - 🎥 Upload any MP4 video  
        - 🧠 AI analyzes faces & artifacts  
        - 📊 Get a confidence score & visual evidence  
        Built for **Hackathon 2025** by **Desi Kalakaaar**.
        """)

st.markdown("---")

# ---------------------
# FILE UPLOAD
# ---------------------
uploaded_video = st.file_uploader("📤 Upload your video (MP4 only)", type=["mp4"])

if uploaded_video:
    # Save video temporarily
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_video.read())

    st.video(video_path)

    # Detect deepfake
    start_time = time.time()
    with st.spinner("🔍 Scanning video for deepfake manipulation... Please wait."):
        results = scan_video(video_path)
    end_time = time.time()

    # ---------------------
    # RESULTS SECTION
    # ---------------------
    st.markdown("## 🧾 Detection Results")
    verdict = results.get("verdict", "Unknown")
    confidence = results.get("confidence", 0)

    if verdict == "REAL":
        st.success(f"✅ Verdict: REAL (Confidence: {confidence}%)")
    elif verdict == "FAKE":
        st.error(f"🚨 Verdict: FAKE (Confidence: {confidence}%)")
    else:
        st.warning("⚠️ Could not determine verdict.")

    # Confidence bar
    st.progress(confidence / 100)

    # Processing time
    st.caption(f"⏱ Processing time: {end_time - start_time:.2f} seconds")

    # ---------------------
    # FRAME PREVIEW
    # ---------------------
    st.markdown("### 📸 Analyzed Frames")
    frame_cols = st.columns(5)
    frames = results.get("frames", [])
    labels = results.get("frame_labels", [])

    fake_count = 0
    real_count = 0

    for idx, frame_path in enumerate(frames):
        with frame_cols[idx % 5]:
            if os.path.exists(frame_path):
                img = Image.open(frame_path)
                if labels and idx < len(labels):
                    if labels[idx] == "FAKE":
                        fake_count += 1
                        st.image(img, caption="FAKE", use_container_width=True)
                    else:
                        real_count += 1
                        st.image(img, caption="REAL", use_container_width=True)
                else:
                    st.image(img, use_container_width=True)

    st.markdown("#### 📊 Frame Analysis Summary")
    st.write(f"✅ REAL frames: {real_count}")
    st.write(f"🚨 FAKE frames: {fake_count}")

    st.markdown("---")
    st.info("📌 Note: This is a demo version for hackathon purposes. Results may not be 100% accurate.")

    if st.button("🔄 Upload Another Video"):
        st.experimental_rerun()
else:
    st.info("📥 Please upload an MP4 video to start detection.")
                     