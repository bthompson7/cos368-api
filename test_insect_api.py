import os
import requests
import base64
import json

data = {}
img_to_open = 'beetle7.jpg'
with open(img_to_open, mode='rb') as file:
    img = file.read()

data['img'] = base64.encodebytes(img)
#data['img'] = 'fsfsdfdsfdsfsdfds'
url = 'http://192.168.1.2:8080/detect'
print(data)
r = requests.post(url=url, data=data)
print(r.status_code, r.reason)
print(r.text)
