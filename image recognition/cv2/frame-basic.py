import cv2 as cv
image = cv.imread('images/1.jpg')
cv.imshow('Photo', image)

#grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

#blur
blur = cv.GaussianBlur(image, (3, 3), cv.BORDER_DEFAULT)
cv.imshow('Blurred Photo', blur)

# edge casade w/o blur
canny = cv.Canny(image, 125, 175)
cv.imshow('Canny Edges w/o Blur', canny)

# edge casade w/ blur
canny = cv.Canny(blur, 125, 175)
cv.imshow('Canny Edges  w/ Blur', canny)

#dilate
dilated = cv.dilate(canny, (3, 3), iterations=3)
cv.imshow('Dilated Canny Edges w/ Blur', dilated)


#eroding
eroded = cv.erode(dilated, (3, 3), iterations=3)
cv.imshow('Eroded Dilated Canny Edges w/ Blur', eroded)

#resize
resized = cv.resize(image, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('Resize', resized)

#cropped
cropped=image[200:400, 200:400]
cv.imshow('Cropped', cropped)

cv.waitKey(0)

