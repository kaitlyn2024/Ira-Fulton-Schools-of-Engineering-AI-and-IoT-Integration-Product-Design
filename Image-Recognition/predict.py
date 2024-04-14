import os

from ultralytics import YOLO
import cv2 as cv


VIDEOS_DIR = 'C:/Users/10000/Desktop/Ira-Fulton-Schools-of-Engineering-AI-and-IoT-Integration-Product-Design/Image-Recognition/cvat/images/test'

video_path = os.path.join(VIDEOS_DIR, 'adonis.mp4')
video_path_out = '{}_out.mp4'.format(video_path)

cap = cv.VideoCapture(video_path)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv.VideoWriter(video_path_out, cv.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv.CAP_PROP_FPS)), (W, H))
print("\nPath: "+str(os.path.join('.', 'Image-Recognition', 'runs', 'detect', 'train3', 'weights', 'last.pt'))+"\n\n")
model_path = os.path.join('.', 'Image-Recognition', 'runs', 'detect', 'train3', 'weights', 'last.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.5

while ret:
    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv.LINE_AA)

    out.write(frame)
    ret, frame = cap.read()

cap.release()
out.release()
cv.destroyAllWindows()