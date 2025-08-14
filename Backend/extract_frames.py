import cv2
import os
import urllib.request

SAMPLE_VIDEO_URL = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
SAMPLE_VIDEO_NAME = "sample.mp4"

def download_sample_video():
    """Download a small sample video if not present."""
    print(f"📥 Downloading sample video from {SAMPLE_VIDEO_URL} ...")
    urllib.request.urlretrieve(SAMPLE_VIDEO_URL, SAMPLE_VIDEO_NAME)
    print(f"✅ Sample video downloaded as {SAMPLE_VIDEO_NAME}")

def extract_frames(video_path, output_folder="frames"):
    # --------------------------
    # 1️⃣ If file not found, auto-download sample
    # --------------------------
    if not os.path.exists(video_path):
        print(f"⚠️ Video file not found: {video_path}")
        print("💡 Downloading sample video instead...")
        download_sample_video()
        video_path = SAMPLE_VIDEO_NAME

    # --------------------------
    # 2️⃣ Try to open video
    # --------------------------
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"❌ Could not open video file: {video_path}\n"
                      f"💡 Possible reasons:\n"
                      f"   - File is corrupted or not a real video.\n"
                      f"   - Wrong path (check case-sensitive names on Mac).\n"
                      f"   - Unsupported codec (try re-encoding with ffmpeg).")

    # --------------------------
    # 3️⃣ Create output folder
    # --------------------------
    os.makedirs(output_folder, exist_ok=True)

    frame_paths = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_path = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path, frame)
        frame_paths.append(frame_path)
        frame_count += 1

    cap.release()

    if frame_count == 0:
        raise ValueError("❌ No frames extracted. The video might be empty or unreadable.")

    print(f"✅ Extracted {frame_count} frames to '{output_folder}'")
    return frame_paths


# --------------------------
# Example run
# --------------------------
if __name__ == "__main__":
    frames = extract_frames("assets/sample.mp4")  # Replace with your path if available
    print("First 5 frames:", frames[:5])
