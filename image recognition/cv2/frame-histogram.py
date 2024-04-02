import cv2 as cv
import matplotlib.pyplot as plt
image = cv.imread('images/3.jpg')
cv.imshow('Bug Photo', image)


# gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
# cv.imshow('Bug Photo', gray)

# grayHistogram= cv.calcHist([gray], [0], None, [256], [0, 256])

# plt.figure()
# plt.title('Grayscale historgram')
# plt.xlabel('Bins')
# plt.ylabel('# of Pixels')
# plt.plot(grayHistogram)
# plt.xlim([0, 256])
# plt.show()

colors = ('b', 'r', 'g')
for i, color in enumerate(colors):
    hist = cv.calcHist([image], [i], None, [256], [0, 256])
    plt.plot(hist, color=color)
    plt.xlim([0, 256])
plt.title('Colors')
plt.xlabel('Bins')
plt.ylabel('# of Pixels')
plt.show()

    

cv.waitKey(0)
