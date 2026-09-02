import cv2
from datetime import datetime

# Open webcam
camera = cv2.VideoCapture(0)

# Set camera resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#Creating our background subtractor
background_subtractor = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=50,
    detectShadows=True
)

while True:
    # Read frame from webcam
    success, frame = camera.read()

    if not success:
        print("Could not access camera.")
        break

    # Flipping frame so it feels like a mirror
    frame = cv2.flip(frame, 1)
