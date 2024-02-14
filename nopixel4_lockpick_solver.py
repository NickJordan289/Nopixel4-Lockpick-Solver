import numpy as np  # Math
import cv2  # Computer vision
import pyautogui  # Button pressing
import mss  # Screen grabbing
import time  # Sleep
from helpers import rotate_image, colour_to_name

# Config
SLICE_WIDTH = 10
SPOKES = 12
RINGS = 5
RING_OFFSET = 50
DEBUG = False
CAPTURE_ZONE = {"top": 236, "left": 3017, "width": 580,
                "height": 580}  # Inner zone around game


def find_layers(img):
    img_width = img.shape[1]
    img_height = img.shape[0]

    rings = [["" for _ in range(SPOKES)] for _ in range(RINGS)]
    circles = [["" for _ in range(SPOKES)] for _ in range(RINGS)]

    for i in range(SPOKES):
        rotated = rotate_image(img, 360/SPOKES*i)
        slice = rotated[0:img_height//2, img_width//2 -
                        SLICE_WIDTH:img_width//2+SLICE_WIDTH]

        if DEBUG:
            annotated = cv2.copyMakeBorder(
                slice.copy(), 0, 0, 0, 300, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        for j in range(RINGS):
            ring = slice[225-RING_OFFSET*j:250-RING_OFFSET*j, 0:250]

            circle_pixel = ring[24, 10]
            if DEBUG:
                cv2.circle(annotated, (10, annotated.shape[0]-(RING_OFFSET*j)-40), 2,
                           (0, 255, 0), -1)
                cv2.putText(annotated, colour_to_name(circle_pixel), (50, annotated.shape[0]-(RING_OFFSET*j)-35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(circle_pixel[0]), int(circle_pixel[1]), int(circle_pixel[2])), 1, cv2.LINE_AA)
            circles[j][i] = colour_to_name(circle_pixel)

            line_pixel = ring[10, 10]
            if DEBUG:
                cv2.circle(annotated, (10, annotated.shape[0]-(RING_OFFSET*j)-55), 2,
                           (0, 255, 0), -1)
                cv2.putText(annotated, colour_to_name(line_pixel), (50, annotated.shape[0]-(RING_OFFSET*j)-50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(line_pixel[0]), int(line_pixel[1]), int(line_pixel[2])), 1, cv2.LINE_AA)
            rings[j][i] = colour_to_name(line_pixel)

        if DEBUG:
            cv2.imshow('Annotated', annotated)
            cv2.waitKey(0)
    return rings, circles


def verify_solution(ring, circles):
    solved = True
    for i in range(len(ring)):
        if ring[i] != "unknown" and ring[i] != circles[i]:
            solved = False
            return False
    return solved


def solve_layer(ring, circles):
    if verify_solution(ring, circles):
        return 0
    for i in range(SPOKES):
        # slide the ring to the right
        ring = ring[1:] + ring[:1]
        if verify_solution(ring, circles):
            return i+1
    return 12


def optimize_rotations(rotations):
    if rotations > 6:
        return rotations - 12
    return rotations


if __name__ == "__main__":
    print("running in 2 seconds")
    time.sleep(1)
    print("running in 1 seconds")
    time.sleep(1)
    print("running")
    while True:
        with mss.mss() as sct:
            img = np.array(sct.grab(CAPTURE_ZONE))
        rings, circles = find_layers(img)

        for i in range(len(rings)):
            rotations = optimize_rotations(solve_layer(rings[i], circles[i]))
            if rotations > 0:
                pyautogui.press('right', presses=rotations)
            elif rotations < 0:
                pyautogui.press('left', presses=abs(rotations))
            pyautogui.press('enter')

        print("done")
        print("trying again in 3 seconds")
        time.sleep(3)
