from PIL import Image

T = [
    [0.31399022, 0.63951294, 0.04649755],
    [0.15537241, 0.75789446, 0.08670142],
    [0.01775239, 0.10944209, 0.87256922],
]

invT = [
    [5.47221206, -4.6419601, 0.16963708],
    [-1.1252419, 2.29317094, -0.1678952],
    [0.02980165, -0.19318073, 1.16364789],
]

Ss = {
    "normal": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    "protanopia": [[0, 1.05118294, -0.05116099], [0, 1, 0], [0, 0, 1],],
    "deuteranopia": [[1, 0, 0], [0.9513092, 0, 0.04866992], [0, 0, 1],],
    "tritanopia": [[1, 0, 0], [0, 1, 0], [-0.86744736, 1.86727089, 0],],
}


def matmul(matrix, vector):
    vx, vy, vz = vector
    Mx, My, Mz = matrix
    x = vx * Mx[0] + vy * Mx[1] + vz * Mx[2]
    y = vx * My[0] + vy * My[1] + vz * My[2]
    z = vx * Mz[0] + vy * Mz[1] + vz * Mz[2]
    return x, y, z


def apply(color, filter, rgba=False):
    if rgba:
        r, g, b, a = color
        color = r, g, b
    lms = matmul(T, color)
    lms_filtered = matmul(filter, lms)
    rgb_filtered = matmul(invT, lms_filtered)
    r, g, b = rgb_filtered
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
