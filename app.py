import os
import psycopg2
import json
from flask import Flask, send_file, render_template, request

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
	'  images TEXT NOT NULL'
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
	formdata = request.form
	if "selected_list" in formdata:
		print(formdata["selected_list"])
	return render_template("thank-you.html")


if __name__ == "__main__":
	# Start Server
	app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
	pass