import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

image = cv.imread('images/1.jpg')
cv.imshow('Bug', image)
blank=np.zeros(image.shape[:2], dtype="uint8")

#spaces

#BRG to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

# BRG to HSV
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
cv.imshow('HSV Photo', hsv)
# BRG to LAB
lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)
cv.imshow('LAB Photo', lab)


rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
cv.imshow('RGB', rgb)

#plt.imshow(rgb)
#plt.show()



#colors 
b, g, r = cv.split(image)
cv.imshow('Blue w/o color', b)
cv.imshow('Green w/o color', g)
cv.imshow('Red w/o color', r)

blue=cv.merge([b, blank, blank])
green=cv.merge([blank, g, blank])
red=cv.merge([blank, blank, r])
cv.imshow('Blue w/ color', blue)
cv.imshow('Green w/ color', green)
cv.imshow('Red w/ color', red)


merged = cv.merge([b, g, r])
cv.imshow('Merged Image', merged)
cv.waitKey(0)
