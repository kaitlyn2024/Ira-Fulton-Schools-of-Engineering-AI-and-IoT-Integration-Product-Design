#Kaitlyn - video recorded, edge / object detection  annotator 
import time
import numpy as np
import cv2 as cv
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

#vars
picam2=None	#camera object
duration=10	#recorded video duration (set low for testing purposes)
dimensions=(1456, 1088) #camera resolution
colour = (0, 255, 0)
origin = (0, 30)
font = cv.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2
target_size=dimensions[0]*dimensions[1]*.005	# what pecentage of the frame needs to be active in order for an edge to be considered signifcant 

#functions
def get_file_name():
	#timestamp file name
	return "static/"+time.strftime("%Y%m%d%H%M%S")+".mp4"
def get_temp():
	#mock tempature end point 
	return "##.#F"
def get_humidity():
	#mock humidity end point 
	return "##.#%"
def get_time():
	return time.strftime("%Y-%m-%d %X")
def draw_bounds(m):
	#set returned camera image resoluion
	frame=cv.resize(m.array, dimensions, interpolation=cv.INTER_AREA)
	
	#set color to black and white for
	mask = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

	#blurs as simple noise reduction method
	mask = cv.medianBlur(mask, 5)

	#adaptive threshold  
	mask = cv.adaptiveThreshold(mask, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 5)
	
	#find the edges between
	contours, hiearchies = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		#get countor box
		area = cv.contourArea(contour)
		if area > target_size:
			#draw countour box on frame
			cv.drawContours(m.array, [contour], -1, (255, 0, 0), 3)
			x, y, w, h = cv.boundingRect(contour)
			cv.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0), 3)
def draw_text(m):
	#add sensor data to video
	cv.putText(m.array, "Time: "+get_time(), origin, font, scale, colour, thickness)
	cv.putText(m.array, "Tempature: "+get_temp(), (origin[0], origin[1]+80), font, scale, colour, thickness)
	cv.putText(m.array, "Humidity: "+get_humidity(), (origin[0], origin[1]+120), font, scale, colour, thickness)
def draw(request):
	#current frame of video
	with MappedArray(request, "main") as m:
		draw_bounds(m)
		draw_text(m)


#create video clips
while True:
	# if camera doesn't exist create one
	if picam2==None:
		picam2 = Picamera2()
	#configure camera
	video_config = picam2.create_video_configuration()
	picam2.configure(video_config)
	
	#when frame processed draw
	picam2.post_callback = draw 
	
	#encode to mp4
	encoder = H264Encoder(10000000)
	output = FfmpegOutput(get_file_name(), audio=True)
	
	#record video clip
	picam2.start_recording(encoder, output)
	time.sleep(duration)
	picam2.stop_recording()
