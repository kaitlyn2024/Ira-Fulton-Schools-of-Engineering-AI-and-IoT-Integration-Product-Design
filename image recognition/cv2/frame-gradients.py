import cv2 as cv
import numpy as np
image = cv.imread('images/1.jpg')
cv.imshow('Photo', image)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

#lapacian
lap = cv.Laplacian(gray, cv.CV_64F)
lap = np.uint8(np.absolute(lap))
cv.imshow('Laplacian', lap)

#Sobel
soblex = cv.Sobel(gray, cv.CV_64F, 1, 0)
sobley = cv.Sobel(gray, cv.CV_64F, 0, 1)
sobelxy = cv.bitwise_or(soblex, sobley)
cv.imshow('Sobel X', soblex)
cv.imshow('Sobel Y', sobley)
cv.imshow('Sobel XY', sobelxy)

canny = cv.Canny(gray, 150, 175)
cv.imshow('Canny', canny)
cv.waitKey(0)
