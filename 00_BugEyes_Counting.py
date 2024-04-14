# Code Written by Eathan Ong, Referenced SunFounder Lessons 25, 28, and 29
# !/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import time
import numpy as np
import cv2 as cv
from picamera2 import Picamera2, MappedArray
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# The Ultrasonic Distance Sensor will use GPIO.BOARD Pins 11 and 12
TRIG = 11
ECHO = 12

# The IR Obstacle Sensor will use GPIO.BOARD Pin 13
ObstaclePin = 13

# The Humiditure Sensor will use GPIO.BOARD Pin 15
DHTPIN = 15

# Constants for the Humiture Sensor
MAX_UNCHANGE_COUNT = 100
STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

#vars
humidity="0"
temperature="0"
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
	#mock temperature end point 
	return "Temperature: %s C`" % (temperature)
def get_humidity():
	#mock humidity end point 
	return "Humidity: %s %%"% (humidity) 
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
	cv.putText(m.array, "Temperature: "+get_temp(), (origin[0], origin[1]+80), font, scale, colour, thickness)
	cv.putText(m.array, "Humidity: "+get_humidity(), (origin[0], origin[1]+120), font, scale, colour, thickness)
def draw(request):
	#current frame of video
	with MappedArray(request, "main") as m:
		draw_bounds(m)
		draw_text(m)

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    GPIO.setup(ObstaclePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
# Code for Ultrasonic Sensor taken from 25_ultrasonic_ranging.py, Sunfounder
def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100
    
# Code for Humiture Sensor taken from 28_humiture.py, Sunfounder
def read_dht11_dat():
	GPIO.setup(DHTPIN, GPIO.OUT)
	GPIO.output(DHTPIN, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(DHTPIN, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

	unchanged_count = 0
	last = -1
	data = []
	while True:
		current = GPIO.input(DHTPIN)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break

	state = STATE_INIT_PULL_DOWN

	lengths = []
	current_length = 0

	for current in data:
		current_length += 1

		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			else:
				continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			else:
				continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			else:
				continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			else:
				continue
	if len(lengths) != 40:
		#print ("Data not good, skip")
		return False

	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0

	for length in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	#print ("bits: %s, length: %d" % (bits, len(bits)))
	for i in range(0, len(bits)):
		byte = byte << 1
		if (bits[i]):
			byte = byte | 1
		else:
			byte = byte | 0
		if ((i + 1) % 8 == 0):
			the_bytes.append(byte)
			byte = 0
	#print (the_bytes)
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		#print ("Data not good, skip")
		return False

	return the_bytes[0], the_bytes[2]

def loop():
	# CUSTOM CODE STARTS HERE
	# When this loop starts there will be initally no bugs
	totalBugs = 0
	result = read_dht11_dat()

	# While the code is not being interupted by keyboard input this will be repeated
	while True:
		bugAtEntrance = 0
		bugAtExit = 0
		
		# Calls methods for Humiture and Ultrasonic Sensor
		result = read_dht11_dat()
		dis = distance()		
		time.sleep(0.1)
		
		# Detects when a bug is first spotted at the enterance, this data is used to determine which way the bug is heading
		# If the Bug is first spotted by the Obstacle Sensor (which is on the outside of the house) and then the Ultrasonic Sensor (which is inside the house) we know that a bug has entered
		while (0 == GPIO.input(ObstaclePin) and dis >= 4.5):
			# We keep track of which sensor detected the bug first using bugAtEntrance
			bugAtEntrance = 1
			dis = distance()			
			result = read_dht11_dat()
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
				picame=None
			
		# If a bug has been previously spotted noted by bugAtEntrance AND there are no bugsAtExit AND
		# The IR Sensor AND Ultrasonic Sensor then we know that a bug has officially entered the house
		while (0 == GPIO.input(ObstaclePin) and dis < 4.5 and bugAtEntrance == 1 and bugAtExit == 0):
			dis = distance()			
			totalBugs = totalBugs + 1
			bugAtEntrance = 0
			print ("Bug Entered , Total Bugs: ", totalBugs)
			
			# If a Humiture reading is available the program will print it
			result = read_dht11_dat()
			
			if result:
				humidity, temperature = result
				print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
				print ("\n")
			else:
				while (not result):
					result = read_dht11_dat()
					if result:
						humidity, temperature = result
						print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
						print ("\n")
					
			time.sleep(1)

		# A bug is detected by the Ultrasonic Sensor before the IR Sensor meaning that a bug is trying to leave	
		while (1 == GPIO.input(ObstaclePin) and dis < 4.5):
			dis = distance()			
			bugAtExit = 1
			result = read_dht11_dat()

		# A bug is then detected by both sensors with the intent to leave meaning that it has exited the house				
		while (0 == GPIO.input(ObstaclePin) and dis < 4.5 and bugAtEntrance == 0 and bugAtExit == 1):
			dis = distance()
			if(totalBugs != 0):
				totalBugs = totalBugs - 1
			print ("Bug Left, Total Bugs: ", totalBugs)
			
			result = read_dht11_dat()

			if result:
				humidity, temperature = result
				print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
				print ("\n")
			else:
				while (not result):
					result = read_dht11_dat()
					if result:
						humidity, temperature = result
						print ("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))
						print ("\n")
				
			bugAtExit = 0
			time.sleep(1)

		# This case should never happen but is included to avoid the program stalling	
		while(bugAtEntrance == 1 and bugAtExit == 1):
			bugAtExit = 0
			bugAtEntrance = 0
			dis = distance()
			result = read_dht11_dat()
			time.sleep(1)
	 
        
def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    result = read_dht11_dat()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
