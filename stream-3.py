#Kaitlyn
import time
import numpy as np
import cv2 as cv
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

#vars
picam2=None
duration=10
dimensions=(1456, 1088)
colour = (0, 255, 0)
origin = (0, 30)
font = cv.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2
target_size=1456*1088*.005

#functions
def get_file_name():
	return "static/"+time.strftime("%Y%m%d%H%M%S")+".mp4"
def get_temp():
	return "##.#F"
def get_humidity():
	return "##.#%"
def get_time():
	return time.strftime("%Y-%m-%d %X")
def draw_bounds(m):
	frame=cv.resize(m.array, dimensions, interpolation=cv.INTER_AREA)
	mask = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	size=frame[0 : (mask.shape[0]), 0 : (mask.shape[1]) ]
	mask = cv.adaptiveThreshold(mask, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 5)
	mask = cv.medianBlur(mask, 5)
	contours, hiearchies = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		area = cv.contourArea(contour)
		if area > target_size:
			cv.drawContours(m.array, [contour], -1, (255, 0, 0), 3)
			x, y, w, h = cv.boundingRect(contour)
			cv.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0), 3)
def draw_text(m):
	#cv.putText(m.array, "Object Count: "+str(get_insect_count()), (origin[0], origin[1]+40), font, scale, colour, thickness)
	cv.putText(m.array, "Time: "+get_time(), origin, font, scale, colour, thickness)
	cv.putText(m.array, "Tempature: "+get_temp(), (origin[0], origin[1]+80), font, scale, colour, thickness)
	cv.putText(m.array, "Humidity: "+get_humidity(), (origin[0], origin[1]+120), font, scale, colour, thickness)
def draw(request):
	with MappedArray(request, "main") as m:
		draw_bounds(m)
		draw_text(m)


#video recording
while True:
	print("hello")
	if picam2==None:
		picam2 = Picamera2()
	video_config = picam2.create_video_configuration()
	picam2.configure(video_config)
	picam2.post_callback = draw

	encoder = H264Encoder(10000000)
	output = FfmpegOutput(get_file_name(), audio=True)

	picam2.start_recording(encoder, output)
	time.sleep(duration)
	picam2.stop_recording()
