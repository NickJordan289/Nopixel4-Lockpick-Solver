import cv2
import numpy as np


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result


def colour_to_name(col):
    if (col == [213, 134, 46, 255]).all():
        return "blue"
    elif (col == [97, 39, 202, 255]).all():
        return "red"
    elif (col == [17, 181, 239, 255]).all():
        return "yellow"
    else:
        return "unknown"
