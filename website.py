#Kaitlyn - website server w/ video streaming
from datetime import datetime
import os
from pathlib import Path
from flask import Flask, Response, render_template
from pathlib import Path


def GetFiles():
	files=[]
	times=[]
	times_count=[]
	files=os.listdir('./static')
	files.sort(key=lambda x: os.path.getmtime(os.path.join("static", x)))

	for file in files:
		print(file)
		file_path=os.path.join(os.path.abspath(os.getcwd()), "static", file)
		
		file_data = os.path.getctime(file_path)
		file_date = datetime.fromtimestamp(file_data)
		file_date = file_date.strftime("%m/%d/%Y")
		if file_date in times: 
			index=times.index(file_date)
			times_count[index]=times_count[index]+1
		else:
			times.append(file_date)
			times_count.append(1)

	return files, times, times_count
#create application at route
app = Flask(__name__)

@app.route("/")
def home():
	#get video paths from local directory
	files, times, times_count = GetFiles()
	return render_template('index.html', content=[files[len(files)-1]], times=times, times_count=times_count)
@app.route("/log")
def logs():
	#get video paths from local directory
	files, times, times_count = GetFiles()
	return render_template('logs.html', content=reversed(files)) #use template passing file path
#create server on local network
if __name__=='__main__':
	app.run(host="0.0.0.0", port=5000, threaded=True)

