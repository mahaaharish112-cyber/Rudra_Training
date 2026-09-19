import cv2
import sys
import math


if len(sys.argv) < 2:
    print("Usage: python3 main.py <image_path>")
    sys.exit()

image_path = sys.argv[1]

image = cv2.imread(image_path)

if image is None:
    print("Could not open image")
    sys.exit()


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


lower_red1 = (0, 100, 80)
upper_red1 = (10, 255, 255)

lower_red2 = (170, 100, 80)
upper_red2 = (180, 255, 255)


mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = cv2.bitwise_or(mask1, mask2)


kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


contours, hierarchy = cv2.findContours(
    mask,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)


object_number = 0


print("\n========== RED OBJECT DETECTION ==========\n")


for contour in contours:

    area = cv2.contourArea(contour)

    if area < 300:
        continue


    object_number += 1


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

        center_x = int(moments["m10"] / moments["m00"])
        center_y = int(moments["m01"] / moments["m00"])

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


    print("Object", object_number)
    print("Color      : Red")
    print("Shape      :", shape)
    print("Coordinates: (", center_x, ",", center_y, ")")
    print("Bounding Box:")
    print("  X =", x)
    print("  Y =", y)
    print("  Width  =", w)
    print("  Height =", h)
    print("Area      :", int(area))
    print("------------------------------------------")


    cv2.drawContours(
        image,
        [contour],
        -1,
        (0, 255, 0),
        2
    )


    cv2.rectangle(
        image,
        (x, y),
        (x + w, y + h),
        (255, 0, 0),
        2
    )


    cv2.circle(
        image,
        (center_x, center_y),
        5,
        (0, 0, 255),
        -1
    )


    cv2.putText(
        image,
        shape,
        (x, y - 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


    coordinate_text = f"({center_x},{center_y})"

    cv2.putText(
        image,
        coordinate_text,
        (x, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2
    )


print("\n==========================================")

if object_number == 0:

    print("No red object detected.")

else:

    print("Total red objects:", object_number)

print("==========================================\n")


cv2.imshow("Red Object Detection", image)

cv2.imshow("Red Mask", mask)

cv2.waitKey(0)

cv2.destroyAllWindows()
