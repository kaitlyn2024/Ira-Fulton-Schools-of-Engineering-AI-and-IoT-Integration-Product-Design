import cv2 as cv
image = cv.imread('images/1.jpg')
cv.imshow('Bug Photo', image)



#average blur
average = cv.blur(image, (3, 3))
cv.imshow('Average', average)

#gaussian blur
guass = cv.GaussianBlur(image, (3, 3), 0)

cv.imshow('Gaussian Blur', guass)

#median blur *noise reduction
median = cv.medianBlur(image, 3)
cv.imshow("Median Blur", median)

#bilateral blur *retain edges
bilateral = cv.bilateralFilter(image, 5, 15, 15)
cv.imshow("Bilateral Blur", bilateral)
cv.waitKey(0)
