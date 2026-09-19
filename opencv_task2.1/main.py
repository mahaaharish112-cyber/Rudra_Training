import cv2
import math


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()


lower_red1 = (0, 100, 80)
upper_red1 = (10, 255, 255)

lower_red2 = (170, 100, 80)
upper_red2 = (180, 255, 255)

lower_blue = (90, 100, 80)
upper_blue = (130, 255, 255)


kernel = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE,
    (5, 5)
)


def detect_objects(mask, color_name, frame):

    contours, hierarchy = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 500:
            continue

        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            continue

        approx = cv2.approxPolyDP(
            contour,
            0.02 * perimeter,
            True
        )

        vertices = len(approx)

        x, y, w, h = cv2.boundingRect(contour)

        moments = cv2.moments(contour)

        if moments["m00"] != 0:

            center_x = int(
                moments["m10"] / moments["m00"]
            )

            center_y = int(
                moments["m01"] / moments["m00"]
            )

        else:

            center_x = x + w // 2
            center_y = y + h // 2


        circularity = (
            4 * math.pi * area
            / (perimeter * perimeter)
        )


        if vertices == 3:

            shape = "Triangle"

        elif vertices == 4:

            aspect_ratio = w / float(h)

            if 0.85 <= aspect_ratio <= 1.15:

                shape = "Square"

            else:

                shape = "Rectangle"

        elif vertices == 5:

            shape = "Pentagon"

        elif vertices == 6:

            shape = "Hexagon"

        elif circularity > 0.80:

            shape = "Circle"

        else:

            shape = "Unknown"


        cv2.drawContours(
            frame,
            [contour],
            -1,
            (0, 255, 0),
            2
        )


        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 255, 255),
            2
        )


        cv2.circle(
            frame,
            (center_x, center_y),
            5,
            (0, 0, 255),
            -1
        )


        cv2.putText(
            frame,
            color_name + " " + shape,
            (x, y - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"({center_x}, {center_y})",
            (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )


        print(
            f"{color_name} | "
            f"Shape: {shape} | "
            f"Coordinates: ({center_x}, {center_y})"
        )


while True:

    ret, frame = cap.read()

    if not ret:
        print("Could not read frame")
        break


    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )


    red_mask1 = cv2.inRange(
        hsv,
        lower_red1,
        upper_red1
    )

    red_mask2 = cv2.inRange(
        hsv,
        lower_red2,
        upper_red2
    )

    red_mask = cv2.bitwise_or(
        red_mask1,
        red_mask2
    )


    blue_mask = cv2.inRange(
        hsv,
        lower_blue,
        upper_blue
    )


    red_mask = cv2.morphologyEx(
        red_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    red_mask = cv2.morphologyEx(
        red_mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    blue_mask = cv2.morphologyEx(
        blue_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    blue_mask = cv2.morphologyEx(
        blue_mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    detect_objects(
        red_mask,
        "RED",
        frame
    )


    detect_objects(
        blue_mask,
        "BLUE",
        frame
    )


    cv2.imshow(
        "RUDRA - Red and Blue Object Detection",
        frame
    )


    cv2.imshow(
        "Red Mask",
        red_mask
    )

    cv2.imshow(
        "Blue Mask",
        blue_mask
    )


    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()
