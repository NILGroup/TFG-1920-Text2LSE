#------------------- Librerías Python -------------------#
from flask import Flask, abort, jsonify, request, send_file, make_response
from flask_cors import CORS
import spacy
import os
#------------------- Archivos lógica --------------------#
import video
import pln
import constantes as const

app = Flask(__name__)
CORS(app)

class BadRequest(Exception):
	def __init__(self, message, status=400, payload=None):
		self.message = message
		self.status = status
		self.payload = payload


@app.errorhandler(BadRequest)
def handle_bad_request(error):
	payload = dict(error.payload or ())
	payload['status'] = error.status
	payload['message'] = error.message
	return jsonify(payload), 404


# ---------------------------------------------------------------------------------------------------------
# ------------------------------------ PROCESAMIENTO VIDEO DE UNA PALABRA ---------------------------------
# ---------------------------------------------------------------------------------------------------------

@app.route("/video/<string:palabra>", methods=["GET"])
def getVideoPalabra(palabra):
    if video.existeVideo(palabra):
        videoPalabra = video.getVideoPalabra(palabra)

    else: raise BadRequest('Lo sentimos, la palabra \'' + palabra + '\' no se encuentra en la biblioteca de vídeos de ARASAAC', 404, { 'ext': 1 })

    response = make_response(send_file(videoPalabra.filename, mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'
    
    return response

# ---------------------------------------------------------------------------------------------------------
# ------------------------------------ PROCESAMIENTO VIDEO DE VARIAS PALABRAS -----------------------------
# ---------------------------------------------------------------------------------------------------------


# Procesa la petición realizada a la API para traducir varias palabras
# Si es una palabra -> Busca el video y lo trata en getVideoPalabra(filename)
# Si hay más de una palabra -> Trata la oración en getTextVideo(sentence)
# Si existen todos los videos -> Devuelve el video generado y lo elimina del sistema de ficheros
# Si alguno de los videos no existe -> Devuelve error
@app.route("/video/", methods=["POST"])
def getTextoTraducidoVideo():

	texto = request.form['Texto']
	size = len(texto.split())
	
	if(size == 1):
		
		if video.existeVideo(texto):
			videoPalabra = video.getVideoPalabra(texto)

		else: raise BadRequest('Lo sentimos, la palabra \'' + texto + '\' no se encuentra en la biblioteca de vídeos de ARASAAC', 404, { 'ext': 1 })

		response = make_response(send_file(videoPalabra.filename, mimetype='video/mp4'))
		response.headers['Content-Transfer-Enconding']='base64'

	elif(size > 1):
		doc = pln.TranslateSentence(texto)
		resultado = video.getTextoVideo(doc)
		
		if (resultado['error'] == True):
			raise BadRequest('Lo sentimos, las palabras \'' + resultado['resultado'] + '\' no se encuentran en la biblioteca de vídeos de ARASAAC', 404, { 'ext': 1 })
		else:
			nombreVideo = resultado['resultado']
			response = make_response(send_file(const.pathVideoGenerado + nombreVideo, mimetype='video/mp4'))
			response.headers['Content-Transfer-Enconding']='base64'
			os.remove(const.pathVideoGenerado + nombreVideo)

	return response

# ---------------------------------------------------------------------------------------------------------
# ------------------------------------- PROCESAMIENTO TEXTO A LSE -----------------------------------------
# ---------------------------------------------------------------------------------------------------------

# Procesa la petición realizada a la API para traducir varias palabras
# Trata la oración en pln.py
# Devuelve la frase traducida a sordo
@app.route("/TextoLSE/", methods=["POST"])
def getTextoTraducido():

	text = request.form['Texto']
	response = []
	frase = ""

	doc = pln.TranslateSentence(text)

	for palabra in doc:
		frase += palabra + " "

	response = {"texto" : frase}
	return response

# ---------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO TEXTO A NOMBRE VIDEOS LSE --------------------------------
# ---------------------------------------------------------------------------------------------------------

# Procesa la petición realizada a la API para traducir varias palabras
# Trata la oración en pln.py
# Devuelve la frase traducida con los nombres de los videos que representen cada palabra
@app.route("/TextoLSEVideos/", methods=["POST"])
def getTextoTraducidoNombreVideos():

	text = request.form['Texto']
	response = []
	frase = ""

	doc = pln.TranslateSentence(text)

	for palabra in doc:
		frase += palabra + " "

	response = {"texto" : frase}
	return response




if __name__ == '__main__':
    app.run(port=8080)