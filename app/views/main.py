import secrets
from flask import render_template, jsonify, request, flash, redirect, url_for
import os
from app import app
import random
from app.forms import user as user_forms


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title='Custom WakeWord')


@app.route('/map')
def map():
	return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
	points = [(random.uniform(48.8434100, 48.8634100),
			   random.uniform(2.3388000, 2.3588000))
			  for _ in range(random.randint(2, 9))]
	return jsonify({'points': points})


@app.route('/contact')
def contact():
	return render_template('contact.html', title='Contact')

def store_file(form_audio):
	random_hex=secrets.token_hex(8)
	_,f_ext=os.path.splitext(form_audio.filename)

	if f_ext.lower() != '.wav':
		return None

	filename=random_hex+f_ext
	file_path=os.path.join(app.root_path,'static/demo_audio',filename)
	form_audio.save(file_path)

	return file_path


@app.route('/demo',methods=['POST','GET'])
def demo():	
	form = user_forms.UploadForm()
	if form.validate_on_submit():
		print(request.files)
		form_audio=request.files['file']
		file_path=store_file(form_audio)
		# data=dp.read_image(filepath)
		# prediction,score=dp.chest_xray(data)
		# score=round(score*100)

	return render_template('demo.html',form=form)

