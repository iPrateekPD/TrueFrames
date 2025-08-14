import os
import urllib.request
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
from backend.extract_frames import extract_frames

# --------------------------
# CONFIG
# --------------------------
MODEL_NAME = "prithivMLmods/deepfake-detector-model-v1"
SAMPLE_VIDEO_URL = "https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4"
SAMPLE_VIDEO_NAME = "sample.mp4"

# --------------------------
# DOWNLOAD SAMPLE VIDEO IF MISSING
# --------------------------
def download_sample_video():
    print(f"📥 Downloading sample video from {SAMPLE_VIDEO_URL} ...")
    urllib.request.urlretrieve(SAMPLE_VIDEO_URL, SAMPLE_VIDEO_NAME)
    print(f"✅ Sample video downloaded as {SAMPLE_VIDEO_NAME}")

# --------------------------
# LOAD MODEL
# --------------------------
print("⏳ Loading model...")
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForImageClassification.from_pretrained(MODEL_NAME)
model.eval()
print("✅ Model loaded.")

# --------------------------
# SCAN VIDEO
# --------------------------
def scan_video(video_path):
    # If video missing, auto-download
    if not os.path.exists(video_path):
        print(f"⚠️ Video not found: {video_path}")
        print("💡 Downloading sample video instead...")
        download_sample_video()
        video_path = SAMPLE_VIDEO_NAME

    # Extract frames
    frames = extract_frames(video_path, output_folder="frames")

    frame_labels = []
    fake_count = 0

    for frame_path in frames:
        img = Image.open(frame_path).convert("RGB")
        inputs = processor(images=img, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            label_id = predictions.argmax().item()
            confidence_score = predictions[0][label_id].item() * 100

        label = model.config.id2label[label_id]

        frame_labels.append(label)
        if label.upper() == "FAKE":
            fake_count += 1

    # --------------------------
    # VERDICT
    # --------------------------
    total_frames = len(frames)
    fake_ratio = fake_count / total_frames

    if fake_ratio > 0.5:
        verdict = "FAKE"
        confidence = round(fake_ratio * 100, 2)
    else:
        verdict = "REAL"
        confidence = round((1 - fake_ratio) * 100, 2)

    return {
        "verdict": verdict,
        "confidence": confidence,
        "frames": frames,
        "frame_labels": frame_labels
    }


# --------------------------
# TEST RUN
# --------------------------
if __name__ == "__main__":
    result = scan_video("assets/sample.mp4")  # Change to your uploaded video path if needed
    print(result)
