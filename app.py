from backend.predict import scan_video
import streamlit as st
from PIL import Image
def display_verdict(verdict):
    if verdict == "REAL":
        st.markdown(
            f"""<div style='background-color:#d4edda; color:#155724; padding:1rem; border-radius:10px'>
            ✅ Verdict: <b>{verdict}</b>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div style='background-color:#f8d7da; color:#721c24; padding:1rem; border-radius:10px'>
            ❌ Verdict: <b>{verdict}</b>
            </div>""",
            unsafe_allow_html=True,
        )

import time

# Page config
st.set_page_config(page_title="TrueFrame - Deepfake Detector", layout="centered")

# Title
st.title("🎥 TrueFrame - Deepfake Video Scanner")

# File uploader
uploaded_file = st.file_uploader("📂 Upload a video file", type=["mp4", "avi", "mov"])

def get_results(video_file):
    # Save uploaded file temporarily
    with open("input_video.mp4", "wb") as f:
        f.write(video_file.read())

    # Call your backend model function
    results = scan_video("input_video.mp4")
    return results


# Process video when uploaded
if uploaded_file:
    st.video(uploaded_file)

    with st.spinner("Analyzing video... Please wait"):
        results = get_results(uploaded_file)

    # Show verdict
    display_verdict(results["verdict"])

    st.metric(label="Confidence", value=f"{results['confidence']}%")

    # Show frames
    st.subheader("Detected Frames")
    cols = st.columns(len(results["frames"]))
    for idx, frame_path in enumerate(results["frames"]):
        with cols[idx]:
            img = Image.open(frame_path)
            st.image(img, caption=f"Frame {idx+1}")

    # Download report button
    st.download_button("📄 Download Report", data="This is a sample report", file_name="TrueFrame_Report.txt")

else:
    st.info("👆 Please upload a video file to start scanning.")
