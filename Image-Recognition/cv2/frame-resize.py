import cv2 as cv
video = cv.VideoCapture('videos/1.mp4')

def resize_photo(frame, scale=.3):
    #already existing video, photo, live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
def change_resolution(width, height):
    #live video
    video.set(3, width)
    video.set(4, height)

while True:
    isTrue, frame = video.read() #video frame
    #cv.imshow('Bug Identification', frame) #display #frame
    frame_resized=resize_photo(frame)
    cv.imshow('Bug Identification Resized', frame_resized) #display #frame

    if cv.waitKey(20) & 0xFF==ord('d'): #if d pressed
        break
video.release()
cv.destroyAllWindows()
cv.waitKey(0)
