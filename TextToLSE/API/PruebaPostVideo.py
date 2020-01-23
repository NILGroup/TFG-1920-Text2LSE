from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, make_response

import spacy, os, uuid, requests, json


# #Llamada a la API que une varios videos y lo devuelve
# url = 'http://127.0.0.1:5000/WordToVideo/'
# payload = {'word': "coco"}
# headers = {'content-type': 'application/json'}
# response = requests.post(url, data=json.dumps(payload), headers=headers)

#Llamada a la API que une varios videos y lo devuelve
url = 'http://127.0.0.1:5000/PhraseToVideo/'
payload = {'texto': "yo cocinar"}
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(payload), headers=headers)

