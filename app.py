import os

from flask import Flask, send_file, render_template

app = Flask(__name__)

if 'DATABASE_URL' in os.environ:
	PORT = 80
else:
	PORT = 8080

@app.route("/favicon.ico")
def favicon():
	return send_file("favicon.ico")

@app.route('/')
def main():
	# get all images
	images = dict()
	for subdirectory in os.listdir(os.path.join("static","images")):
		# list all files in the subdirectory and add them to the dictionary
		images[subdirectory] = [x for x in os.listdir(os.path.join("static", "images", subdirectory))
								# check if filename is an acceptable image format
								# Fails if files without a "." are present in the directory TODO
								if x.rsplit(".",1)[1].lower() in ["jpg", "jpeg", "png", "gif"]]

	return render_template("index.html", images=images)


if __name__ == "__main__":
	# Start Server
	app.run(host='0.0.0.0', port=PORT, threaded=True, debug=True)
	pass