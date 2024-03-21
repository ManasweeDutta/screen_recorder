import streamlit as st
from PIL import ImageGrab
import numpy as np
import cv2
from screeninfo import get_monitors

# Webcam overlay parameters (adjust as needed)
webcam_width = 200
webcam_height = 150
webcam_position = "top-right"  # Options: "top-right", "top-left", "bottom-right", "bottom-left"

# Function to start screen recording
def start_screen_recording(file_name, fps=7.0):
    # Get screen dimensions using screeninfo
    monitors = get_monitors()
    screen_width, screen_height = monitors[0].width, monitors[0].height

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    capture_video = cv2.VideoWriter(file_name, fourcc, fps, (screen_width, screen_height))
    cam = cv2.VideoCapture(0)
    while True:
        # Capture entire screen using ImageGrab
        img = ImageGrab.grab()  # Captures the entire screen
        img_np = np.array(img)

        # Capture webcam frame
        _, webcam_frame = cam.read()
        webcam_frame = cv2.resize(webcam_frame, (webcam_width, webcam_height))

        # Combine screen and webcam frame with overlay positioning
        if webcam_position == "top-right":
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            img_final[0:webcam_height, screen_width - webcam_width:, :] = webcam_frame
        elif webcam_position == "top-left":
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            img_final[0:webcam_height, 0:webcam_width, :] = webcam_frame
        elif webcam_position == "bottom-right":
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            img_final[screen_height - webcam_height:, screen_width - webcam_width:, :] = webcam_frame
        elif webcam_position == "bottom-left":
            img_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            img_final[screen_height - webcam_height:, 0:webcam_width, :] = webcam_frame
        else:
            st.error("Invalid webcam position. Please choose from 'top-right', 'top-left', 'bottom-right', or 'bottom-left'.")
            break

        capture_video.write(img_final)
        st.image(img_final, channels="RGB", use_column_width=True)
        if cv2.waitKey(10) == ord('q'):
            break

    # Release resources
    cam.release()
    capture_video.release()

# Main Streamlit code
def main():
    st.title("Screen Recorder with Webcam Overlay")
    st.sidebar.header("Settings")
    file_name = st.sidebar.text_input("Enter file name:", value="recording.mp4")
    fps = st.sidebar.number_input("Frame Rate (FPS)", min_value=1.0, value=7.0)
    webcam_position = st.sidebar.selectbox("Webcam Position", ["top-right", "top-left", "bottom-right", "bottom-left"])
    st.sidebar.write("Note: Using screeninfo library for screen capture (entire screen).")
    start_button = st.sidebar.button("Start Recording")
    if start_button:
        start_screen_recording(file_name, fps)

if __name__ == "__main__":
    main()
