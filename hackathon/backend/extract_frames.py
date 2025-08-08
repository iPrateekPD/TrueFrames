import cv2
import os

def extract_frames(video_path, output_folder="frames", every_nth=30):
    cap = cv2.VideoCapture(video_path)
    os.makedirs(output_folder, exist_ok=True)
    frame_count = 0
    saved = 0

    while True:
        success, frame = cap.read()
        if not success:
            break
        if frame_count % every_nth == 0:
            filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
        frame_count += 1

    cap.release()
    return saved
