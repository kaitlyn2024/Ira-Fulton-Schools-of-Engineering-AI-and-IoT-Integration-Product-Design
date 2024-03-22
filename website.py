import time
import os
from flask import Flask, Response, render_template, url_for

#vars

#functions
def get_file_name():
	return "static/"+time.strftime("%Y%m%d%H%M%S")+".mp4"



#application
app = Flask(__name__)
@app.route("/")
def hello_world():
	files=os.listdir('./static')
	return render_template('index.html', content=files)

if __name__=='__main__':
	app.run(host="0.0.0.0", port=5000, threaded=True)

