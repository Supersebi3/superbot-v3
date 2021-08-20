import numpy as np
from PIL import Image

T = np.array([
    [0.31399022, 0.63951294, 0.04649755],
    [0.15537241, 0.75789446, 0.08670142],
    [0.01775239, 0.10944209, 0.87256922],
])

invT = np.array([
    [5.47221206, -4.6419601, 0.16963708],
    [-1.1252419, 2.29317094, -0.1678952],
    [0.02980165, -0.19318073, 1.16364789],
])

Ss = {
    "normal": np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
    "protanopia": np.array([[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1],]),
    "deuteranopia": np.array([[1, 0, 0], [0.9513092, 0, 0.04866992], [0, 0, 1],]),
    "tritanopia": np.array([[1, 0, 0], [0, 1, 0], [-0.86744736, 1.86727089, 0],]),
}


def apply(color, filter, rgba=False):
    if rgba:
        r, g, b, a = color
        color = r, g, b
    filtered = invT @ filter @ T @ color
    r, g, b = filtered
    if rgba:
        return round(r), round(g), round(b), a
    return round(r), round(g), round(b)


def apply_image(image, filter):
    img = image.copy()
    rgba = img.mode == "RGBA"
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            col = px[x, y]
            px[x, y] = apply(col, filter, rgba)
    return img


def protanopia(img):
    return apply_image(img, Ss["protanopia"])


def deuteranopia(img):
    return apply_image(img, Ss["deuteranopia"])


def tritanopia(img):
    return apply_image(img, Ss["tritanopia"])
