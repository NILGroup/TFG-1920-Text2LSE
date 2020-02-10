from flask import Flask, jsonify, redirect, url_for, request, Response, json
from flask import render_template
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, make_response
from moviepy.editor import VideoFileClip, concatenate_videoclips

import spacy
import os
import uuid
import shutil
import video.py


nlp = spacy.load("es_core_news_md")
doc = nlp("Yo como patatas")

app = Flask(__name__)
CORS(app)

app.config["videos"] = "videos/"


url = "videos/"



# ----------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA --------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------



# Procesa la petición realizada a la API para traducir una sola palabra
# Busca el video y lo trata en getWordVideo(palabra)
# Si existe el video -> Lo devuelve y lo elimina del sistema de ficheros
# Si no existe -> Devuelve error
@app.route("/TranslateWord/", methods=["GET"])
def videoWordProcessing(id):

	videoName = getWordVideo(id)
	videoName = url + id + ".mp4"
	if (videoName == 404):
	    abort(404, message="No existe el video " + filename + ".mp4 indicado.")
	else:
		response = make_response(send_file(videoName, mimetype='video/mp4'))
		response.headers['Content-Transfer-Enconding']='base64'
		os.remove(videoName)

	return response

# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ PROCESAMIENTO VIDEO DE VARIAS PALABRA -------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------

# Comprobar que todos los videos de la frase están en la carpeta /videos 
# Si todos los videos existen -> Los mete en un array y los concatena, genera el video temporal y devuelve el nombre del video generado 
# Si no encuentra alguno de los videos -> Devuelve error
def getTextVideo(sentence):

	videos = []
	print(sentence)

	for token in sentence:
		if os.path.isfile(url + token.text +".mp4"):
			print(token.text + " " +  "Found")
			clip = VideoFileClip("videos/" + token.text+  ".mp4")
			videos.append(clip)
		else:
			print(token.text + " " + "Not Found")


	idVideo = str(uuid.uuid4())
	final_clip = concatenate_videoclips(videos)
	final_clip.write_videofile(idVideo + ".mp4")

	return idVideo + ".mp4"

#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------

# Procesa la petición realizada a la API para traducir varias palabras
# Si es una palabra -> Busca el video y lo trata en getWordVideo(filename)
# Si hay más de una palabra -> Trata la oración en getTextVideo(sentence)
# Si existen todos los videos -> Devuelve el video generado y lo elimina del sistema de ficheros
# Si alguno de los videos no existe -> Devuelve error
@app.route("/TranslateText/", methods=["POST"])
def getTranslateText():

	text = request.form['TextToTranslate']
	doc = nlp(text)
	size = len(text.split())

	tokens = []
	videos = []
	

	if(size == 1):
		
		videoName = getWordVideo(text)

		if (videoName == "error"):
			#Tratar excepcion
			print ("Video no encontrado")
		else:
			response = make_response(send_file(videoName, mimetype='video/mp4'))
			response.headers['Content-Transfer-Enconding']='base64'
			os.remove(videoName)

	elif(size > 1):
		
		videoName = getTextVideo(doc)

		if (videoName == "error"):
			#Tratar excepcion
			print ("Video no encontrado")
		else:
			response = make_response(send_file(videoName, mimetype='video/mp4'))
			response.headers['Content-Transfer-Enconding']='base64'
			os.remove(videoName)


	return response
	
# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------	


if __name__ == '__main__':
	app.run(port=8080)
