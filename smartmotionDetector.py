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

    # Get the foreground mask
    mask = background_subtractor.apply(frame)

    # Remove the shadows
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)

    # Reduce the  noise
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (5, 5)
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find any moving objects in my webcam
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    motion_detected = False
    motion_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        # Ignore tiny movements/noise
        if area < 2000:
            continue

        motion_detected = True
        motion_area += area

        # Get the  moving object's position
        x, y, w, h = cv2.boundingRect(contour)

        # Draw box around movement
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Label the moving object
        cv2.putText(
            frame,
            "MOVEMENT",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Calculate the approximate motion percentage
    frame_area = frame.shape[0] * frame.shape[1]
    motion_percentage = (motion_area / frame_area) * 100

    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # Draw top information bar
    cv2.rectangle(
        frame,
        (0, 0),
        (frame.shape[1], 70),
        (0, 0, 0),
        -1
    )

    # Show motion status
    if motion_detected:
        status = "MOTION DETECTED"
        status_color = (0, 0, 255)
    else:
        status = "NO MOTION"
        status_color = (0, 255, 0)

    cv2.putText(
        frame,
        status,
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        status_color,
        2
    )
