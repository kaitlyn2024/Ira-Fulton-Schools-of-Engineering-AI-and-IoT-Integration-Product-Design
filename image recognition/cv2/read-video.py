import cv2 as cv
video = cv.VideoCapture('videos/1.mp4')
while True:
    isTrue, frame = video.read() #video frame
    cv.imshow('Read Video', frame) #display #frame

    if cv.waitKey(20) & 0xFF==ord('d'): #if d pressed
        break
video.release()
cv.destroyAllWindows()