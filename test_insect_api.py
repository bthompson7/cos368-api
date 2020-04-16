import os
import requests
import base64
import json

data = {}
img_to_open = 'hornworm5.jpg'
with open(img_to_open, mode='rb') as file:
    img = file.read()

data['img'] = base64.encodebytes(img).decode("utf-8")

url = 'http://192.168.1.2:8080/detect'
r = requests.post(url=url, data=data)
print(r.status_code, r.reason)
print(r.text)
