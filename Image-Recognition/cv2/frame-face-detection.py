import cv2 as cv
image = cv.imread('images/game-changer.jpeg')
cv.imshow('D&D Guy', image)

gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow('Grayscale Photo', gray)

haar_cascade = cv.CascadeClassifier('haar_face.xml')

faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)


print(f'Number of faces found {len(faces_rect)}')
for (x, y, w, h) in faces_rect:
    cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)
cv.imshow('Dectected Faces', image)
cv.waitKey(0)
