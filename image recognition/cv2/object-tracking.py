import cv2 as cv
video = cv.VideoCapture('videos/3.mp4')
dimensions=(1456, 1088)
insect_count=0
#object_detector = cv.createBackgroundSubtractorMOG2()
while True:
    isTrue, frame = video.read() #video frame
    frame=cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
    mask = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    size=frame[0 : (mask.shape[0]), 0 : (mask.shape[1]) ]
    #mask = cv.bilateralFilter(mask, 5, 15, 15)
    mask = cv.medianBlur(mask, 11)
    mask = cv.adaptiveThreshold(mask, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 5)

    #mask = cv.adaptiveThreshold(mask, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 9)
    #mask = cv.Canny(mask, 150, 175)
    contours, hiearchies = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    insect_count=-1
    for contour in contours:
        area = cv.contourArea(contour)
        if area > 5000:
            cv.drawContours(frame, [contour], -1, (255, 0, 0), 3)
            x, y, w, h = cv.boundingRect(contour)
            cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            insect_count+=1
    cv.putText(frame, str(insect_count), (frame.shape[1]//2, frame.shape[0]//2), cv.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)

    
    cv.imshow('Bug Counter', frame) #display #frame

    if cv.waitKey(20) & 0xFF==ord('d'): #if d pressed
        break
video.release()
cv.destroyAllWindows()