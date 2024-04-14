import cv2 as cv
import numpy as np

image = cv.imread('images/1.jpg')
cv.imshow('Bug', image)

#translate
def translate(image, x, y):
    # -x : left, +x : right;  - y: up, +y : down;
    translationMatrix = np.float32([[1, 0, x], [0, 1, y]])
    dimensions=(image.shape[1], image.shape[0])
    return cv.warpAffine(image, translationMatrix, dimensions)

translated=translate(image, 100, 100)
cv.imshow('Translated', translated)

#rotate
def rotate(image, angle, rotationPoint=None):
    (height, width) = image.shape[:2]
    if rotationPoint is None:
        rotationPoint = (width//2, height//2)
    rotatedMatrix = cv.getRotationMatrix2D(rotationPoint, angle, 1.0)
    dimensions=(width, height)
    return cv.warpAffine(image, rotatedMatrix, dimensions)

rotated=rotate(image, 45)
cv.imshow('Rotated', rotated)


#resize
resized = cv.resize(image, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resize', resized)


#resize
# 0 : vertical, 1 : horizontal, -1 : both
flipped = cv.flip(image, 0)
cv.imshow('Flipped', flipped)

#cropped
cropped=image[200:400, 200:400]
cv.imshow('Cropped', cropped)

cv.waitKey(0)
