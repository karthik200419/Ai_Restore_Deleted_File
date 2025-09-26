import cv2
import os
import torch
from torchvision.transforms import ToTensor, ToPILImage
from PIL import Image

class VideoReconstructor:
    def __init__(self):
        print("[*] Video Reconstruction Module Initialized")

    def extract_frames(self, video_path, output_dir="temp_frames"):
        if not os.path.exists(video_path):
            print("[!] Video file not found.")
            return None

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_path = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
            cv2.imwrite(frame_path, frame)
            frame_count += 1

        cap.release()
        print(f"[+] Extracted {frame_count} frames to {output_dir}")
        return output_dir

    def reconstruct_frame(self, frame_path):
        """
        Dummy reconstruction: Convert frame to grayscale for demo.
        Replace this with AI inpainting for real reconstruction.
        """
        frame = Image.open(frame_path).convert("RGB")
        frame = frame.convert("L")  # Grayscale conversion
        frame.save(frame_path)
        return frame_path

    def reconstruct_video(self, frames_dir, output_video_path, fps=30):
        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".png")])
        if not frame_files:
            print("[!] No frames found.")
            return None

        first_frame = cv2.imread(os.path.join(frames_dir, frame_files[0]))
        height, width, _ = first_frame.shape
        out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            frame = cv2.imread(frame_path)
            out.write(frame)

        out.release()
        print(f"[+] Reconstructed video saved: {output_video_path}")
        return output_video_path

    def reconstruct(self, video_path, output_path="reconstructed_video.mp4"):
        frames_dir = self.extract_frames(video_path)
        if not frames_dir:
            return None

        for frame_file in os.listdir(frames_dir):
            frame_path = os.path.join(frames_dir, frame_file)
            self.reconstruct_frame(frame_path)

        return self.reconstruct_video(frames_dir, output_path)
