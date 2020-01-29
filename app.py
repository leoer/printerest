import os
import psycopg2
import time
import json
from flask import Flask, send_file, render_template, request, jsonify

app = Flask(__name__)

# connect to database
if 'DATABASE_URL' in os.environ:
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
else:
	conn = psycopg2.connect("host=localhost dbname=printerest")

# setup database
create_chosen_images = (
	'CREATE TABLE IF NOT EXISTS chosen_images '
	'('
	'  id SERIAL PRIMARY KEY,'
	'  images TEXT NOT NULL,'
	'  timestamp bigint NOT NULL'
	')'
)
with conn, conn.cursor() as cur:
	cur.execute(create_chosen_images)



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

@app.route('/thank-you', methods=["GET", "POST"])
def thank_you():
	# TODO: Prevent double submissions (set cookie?)
	formdata = request.form
	if "selected_list" in formdata:
		selected_list = formdata["selected_list"]
		with conn, conn.cursor() as cur:
			cur.execute("INSERT INTO chosen_images (images, timestamp) VALUES (%s, %s	)", (selected_list, int(time.time()*1000)))
	return render_template("thank-you.html")

@app.route('/api')
def printer_api():
	if not "timestamp" in request.args:
		return ""
	timestamp = int(request.args["timestamp"])
	with conn, conn.cursor() as cur:
		cur.execute("SELECT * FROM chosen_images WHERE timestamp > %s", (timestamp,))
		existing = cur.fetchall()
	existing = [[id, json.loads(images), timestamp] for id, images, timestamp in existing]
	return jsonify(existing)

if __name__ == "__main__":
	# Start Server
	app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
	pass