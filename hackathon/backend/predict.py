from backend.extract_frames import extract_frames
import random
import os

def scan_video(video_path):
    extract_frames(video_path)

    # Pick 2 random frames to "fake"
    frame_files = sorted(os.listdir("frames"))
    selected_frames = random.sample(frame_files, 2) if len(frame_files) >= 2 else frame_files

    return {
        "verdict": "FAKE",
        "confidence": random.randint(60, 95),
        "frames": [f"frames/{f}" for f in selected_frames]
    }
