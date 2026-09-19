import cv2
import numpy as np


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()


while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read frame")
        break


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    minimum = np.min(gray)
    maximum = np.max(gray)
    average = np.mean(gray)


    print(
        f"Min: {minimum:3.0f} | "
        f"Max: {maximum:3.0f} | "
        f"Average: {average:6.2f}"
    )


    cv2.imshow(
        "Grayscale Webcam",
        gray
    )


    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()
