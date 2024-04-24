#Kaitlyn - website server w/ video streaming
from datetime import datetime
import os
from flask import Flask, Response, render_template, url_for
import json

#create application at route
app = Flask(__name__)
@app.route("/")
def home():
	#get video paths from local directory
	files=os.listdir('./static')
	times=[1]
	time_count=[1]
	temperature=[1]	
	humidity=[1]
	bug_count=[1]
	with  open("bugs.json", "r+") as file:
		file_data = json.load(file)
		for value in file_data["bug_logs"]:
			value = json.loads(value)
			times.append(value["time"])
			temperature.append(value["temperature"])
			humidity.append(value["humidity"])
			bug_count.append(value["bug_count"])

	return render_template('index.html', content=[files[0]], times=times, temperature=temperature, humidity=humidity, bug_count=bug_count)
@app.route("/log")
def logs():
	#get video paths from local directory
	files=os.listdir('./static')
	return render_template('logs.html', content=files) #use template passing file path
@app.route("/feed")
def feed():
	#get video paths from local directory
	files=os.listdir('./static')
	return render_template('feed.html', content=files) #use template passing file path

#create server on local network
if __name__=='__main__':
	app.run(host="0.0.0.0", port=5000, threaded=True)

