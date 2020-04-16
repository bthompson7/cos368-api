import os,requests
from flask import Flask,render_template,jsonify, request
from twisted.internet import reactor
from twisted.web.proxy import ReverseProxyResource
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
import os.path
import numpy as np
import keras
from keras.models import load_model
from skimage.io import imread
from skimage.transform import resize
import json
import re
from io import BytesIO
from PIL import Image
import base64
import h5py

app = Flask(__name__)
#app.config["DEBUG"] = True

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error="Resource not found"), 404

'''

returns a json representation of the guess
example:

{
  "img_guess": "Beetle"
}


'''

@app.route('/detect', methods=['POST'])
def detectInsect():
	image_data = request.form['img']
	image_bytes = str.encode(image_data)
	type(image_bytes)
	class_labels = {0: 'Hornworm', 1: 'Beetle'}
	model = load_model('insect_model.h5') #the model can detect Hornworms and Beetles for now
	print("reading image...")
	image_to_test = 'beetle_api_test.jpg'
	with open(image_to_test, "wb") as fh:
		 fh.write(base64.decodebytes(image_bytes))

	img = imread(image_to_test)
	img = resize(img, (150, 150))
	img = np.expand_dims(img, axis=0)
	if(np.max(img)>1):
    		img = img/255.0
	pred = model.predict_classes(img,verbose=1)
	guess = class_labels[pred[0][0]]
	print("I think its a %s"%guess)
	return jsonify(img_guess=guess)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)
reactor.listenTCP(8080, site)
reactor.run()



