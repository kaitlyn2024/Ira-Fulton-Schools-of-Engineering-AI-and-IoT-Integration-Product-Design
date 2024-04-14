# contours
import cv2 as cv
import numpy as np
useCanny=False
image = cv.imread('images/1.jpg')
cv.imshow('Bug', image)

blank = np.zeros(image.shape, dtype="uint8")
cv.imshow('bBank', blank)

#grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

#blur
image = cv.GaussianBlur(image, (3, 3), cv.BORDER_DEFAULT)
cv.imshow('Blurred Photo', image)


if useCanny:
    # edge casade 
    canny = cv.Canny(image, 125, 175)
    cv.imshow('Canny Edges Photo', canny)

    contours, hierarchies=cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(blank, contours, -1, (0, 0, 255), 1)
    cv.imshow('Canny Contours', blank)

else:
    ret, thresh = cv.threshold(gray, 125, 255, cv.THRESH_BINARY)
    cv.imshow('Thresh Photo', thresh)

    contours, hierarchies=cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    cv.drawContours(blank, contours, -1, (0, 0, 255), 1)
    cv.imshow('Thresh Contours', blank)


cv.waitKey(0)
