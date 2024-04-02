#Kaitlyn - website server w/ video streaming
import time
import os
from flask import Flask, Response, render_template, url_for

#create application at route
app = Flask(__name__)
@app.route("/")
def hello_world():
	#get video paths from local directory
	files=os.listdir('./static')
	return render_template('index.html', content=files) #use template passing file path

#create server on local network
if __name__=='__main__':
	app.run(host="0.0.0.0", port=5000, threaded=True)

