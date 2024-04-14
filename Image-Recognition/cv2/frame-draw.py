import cv2 as cv
import numpy as np
#blank
blank = np.zeros((500, 500, 3), dtype='uint8')
cv.imshow('Blank', blank)

#green
blank[:] = 0, 255, 0
cv.imshow('Green', blank)

#square 
blank[:] = 0, 0, 0
cv.rectangle(blank, (0, 0), (250, 250), (255, 0, 0), thickness=2)
cv.imshow('Square', blank)

#square relative
blank[:] = 0, 0, 0
cv.rectangle(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//2), (255, 0, 0), thickness=-1)
cv.imshow('Square Relative', blank)

#circle
blank[:] = 0, 0, 0
cv.circle(blank, (blank.shape[1]//2, blank.shape[0]//2), 50, (0, 0, 250), thickness=3)
cv.imshow('Circle', blank)


#line
blank[:] = 0, 0, 0
cv.line(blank, (0, 0), (blank.shape[1]//2, blank.shape[0]//2), (255, 255, 255), thickness=2)
cv.imshow('Line', blank)

#text
blank[:] = 0, 0, 0
cv.putText(blank, "Hello", (blank.shape[1]//2, blank.shape[0]//2), cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
cv.imshow('Text', blank)

cv.waitKey(0)