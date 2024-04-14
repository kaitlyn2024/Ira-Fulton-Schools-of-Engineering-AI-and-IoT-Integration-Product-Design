import cv2 as cv
import numpy as np
image = cv.imread('images/1.jpg')
cv.imshow('Photo', image)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

#simple threshold
threshhold, thresh = cv. threshold(gray, 150, 255, cv.THRESH_BINARY)
cv.imshow('Simple Threshhold', thresh)


#simple threshold
threshhold, thresh = cv. threshold(gray, 150, 255, cv.THRESH_BINARY_INV)
cv.imshow('Simple Threshhold Inverse', thresh)

#adaptive threshold
adaptive_thresh = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 9)
cv.imshow('Adaptive Threshhold', adaptive_thresh)

cv.waitKey(0)
