import os

from flask import Flask, send_file

app = Flask(__name__)

if 'DATABASE_URL' in os.environ:
	PORT = 80
else:
	PORT = 8080

@app.route("/favicon.ico")
def favicon():
	return send_file("favicon.ico")

@app.route('/')
def hello_world():
	return 'Hello World!'


if __name__ == "__main__":
	# Start Server
	app.run(host='0.0.0.0', port=PORT, threaded=True)
	pass