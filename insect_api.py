import os,requests
from flask import Flask,render_template,jsonify, request
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import numpy as np
from keras.models import load_model
from skimage.io import imread
from skimage.transform import resize
import json,re,h5py,base64,keras
from io import BytesIO
from PIL import Image

app = Flask(__name__)
#app.config["DEBUG"] = True

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Resource not found"), 404

'''
Attempts to guess the insect in an image

    Returns:
        the guess in json

Make sure to send the api an image in base64 and then turn that into json so that
the api can read it

Then it would return:

200 OK
{"img_guess":"Hornworm","is_pest":"yes"}

'''
pests = ["Hornworm","Japanese Beetle","Browntail Moth"]
@app.route('/detect', methods=['POST'])
def detectInsect():
	image_data = request.form['img']
	image_bytes = str.encode(image_data)
	type(image_bytes)
	class_labels = {0: 'Browntail Moth', 1: 'Hornworm',2: 'Japanese Beetle', 3:'Ladybug'}
	model = load_model('insect_model2.h5') #the model can detect Hornworms and Beetles for now
	print("reading image...")
	image_to_test = 'image_to_test.jpg'
	with open(image_to_test, "wb") as fh:
		 fh.write(base64.decodebytes(image_bytes))

	img = imread(image_to_test)
	img = resize(img, (150, 150))
	img = np.expand_dims(img, axis=0)
	if(np.max(img)>1):
    		img = img/255.0
	pred = model.predict_classes(img,verbose=1)
	guess = class_labels[pred[0]]
	print("I think its a %s"%guess)

	is_pest = 'no'
	for insect in pests:
		if guess == insect:
			is_pest = 'yes'
	return jsonify(img_guess=guess,is_pest=is_pest)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(8080, site)
reactor.run()



