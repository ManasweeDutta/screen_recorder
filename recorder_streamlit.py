import streamlit as st
from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics

# Function to start screen recording
def start_screen_recording(file_name, width, height):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    capture_video = cv2.VideoWriter(file_name, fourcc, 10.0, (width, height))
    cam = cv2.VideoCapture(0)
    while True:
        img = ImageGrab.grab(bbox=(0, 0, width, height))
        img_np = np.array(img)
        img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        p, frame = cam.read()
        fr_height, fr_width, _ = frame.shape
        img_final[0:fr_height, 0: fr_width, :] = frame[0: fr_height, 0: fr_width, :]
        capture_video.write(img_final)
        st.image(img_final, channels="RGB", use_column_width=True)
        if cv2.waitKey(10) == ord('q'):
            break

# Main Streamlit code
def main():
    st.title("Screen Recorder")
    st.sidebar.header("Settings")
    file_name = st.sidebar.text_input("Enter file name:", value="recording.mp4")
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    st.sidebar.write(f"Screen resolution: {width}x{height}")
    start_button = st.sidebar.button("Start Recording")
    if start_button:
        start_screen_recording(file_name, width, height)

if __name__ == "__main__":
    main()
