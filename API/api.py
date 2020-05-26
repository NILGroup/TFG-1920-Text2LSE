#------------------- Librerías Python -------------------#
from flask import Flask, abort, jsonify, request, send_file, make_response
from flask_cors import CORS
import spacy, os
#------------------- Archivos lógica --------------------#
import video, imagenes, pln
import constantes as const

app = Flask(__name__)
CORS(app)


#------------------- Gestion de errores --------------------#
class BadRequest(Exception):
	def __init__(self, message, status=400, payload=None):
		self.message = message
		self.status  = status
		self.payload = payload


@app.errorhandler(BadRequest)
def handle_bad_request(error):
	payload = dict(error.payload or ())
	payload['status'] = error.status
	payload['message'] = error.message
	return jsonify(payload), 404
#-----------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------
# ------------------------------------ PROCESAMIENTO VIDEO DE UNA PALABRA ---------------------------------
# ---------------------------------------------------------------------------------------------------------
@app.route("/video/<string:palabra>", methods=["GET"])
def getVideoPalabra(palabra):
	
	if video.existeVideo(palabra.lower()):
		resultado = video.getVideoPalabra(palabra.lower())
		

	else: 
		#raise BadRequest('Lo sentimos, la palabra \'' + palabra + '\' no se encuentra en la biblioteca de vídeos de ARASAAC', 404, { 'ext': 1 })
		resultado = video.getVideoPalabra("error404")


	response = make_response(send_file(resultado.filename, mimetype='video/mp4'))
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

	doc = pln.TranslateSentence(texto)
	frase = video.getTextoVideo(doc)

	nombreVideo = video.getVideoTexto(frase)
	response = make_response(send_file(const.pathVideoGenerado + nombreVideo, mimetype='video/mp4'))
	response.headers['Content-Transfer-Enconding']='base64'
	os.remove(const.pathVideoGenerado + nombreVideo)

	return response

	# texto = request.form['Texto']
	# size = len(texto.split())

	# doc = pln.TranslateSentence(texto)
	# resultado = video.getTextoVideo(doc)

	# if (resultado['error'] == True):
	# 	raise BadRequest('Lo sentimos, las palabras \'' + resultado['resultado'] + '\' no se encuentran en la biblioteca de vídeos de ARASAAC', 404, { 'ext': 1 })
	# else:
	# 	nombreVideo = video.getVideoTexto(resultado['resultado'])
	# 	response = make_response(send_file(const.pathVideoGenerado + nombreVideo, mimetype='video/mp4'))
	# 	response.headers['Content-Transfer-Enconding']='base64'
	# 	os.remove(const.pathVideoGenerado + nombreVideo)

	# 	return response
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
# -------------------------------- PROCESAMIENTO PALABRA A IMAGEN LSE -------------------------------------
# ---------------------------------------------------------------------------------------------------------
@app.route("/imagen/<string:palabra>", methods=["GET"])
def getImagenPalabra(palabra):
	
	if imagenes.existeImagen(palabra.lower()):
		resultado = imagenes.getImagenPalabra(palabra.lower())

	else:  
		#raise BadRequest(palabra, 404, { 'ext': 1 })
		resultado = imagenes.getImagenPalabra("error404")

	response = make_response(send_file(resultado, mimetype='image/jpeg'))
	response.headers["Content-Type"] = "charset=utf-8"
	response.headers["Content-Type"] = "image/jpeg"
	response.headers['Content-Transfer-Enconding']='base64'
	
	return response

# ---------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO TEXTO A TEXTO PARA IMAGENES LSE -------------------------------------
# ---------------------------------------------------------------------------------------------------------
@app.route("/textoImagen/", methods=["POST"])
def getTextoTraducidoImagen():
	
	texto = request.form['Texto']

	doc = pln.TranslateSentence(texto)
	frase = imagenes.getTextoImagenes(doc)
	response = make_response(jsonify(frase = frase))
	

	# if (resultado['error'] == True):
	# 	raise BadRequest(resultado['resultado'], 404, { 'ext': 1 })
	# else:
	# 	frase = resultado['resultado']
	# 	response = make_response(jsonify(frase = frase))
		
	return response


# ---------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO TEXTO A NOMBRE VIDEOS LSE --------------------------------
# ---------------------------------------------------------------------------------------------------------

# Procesa la petición realizada a la API para traducir varias palabras
# Trata la oración en pln.py
# Devuelve la frase traducida con los nombres de los videos que representen cada p
@app.route("/TextoLSEVideos/", methods=["POST"])
def getTextoTraducidoNombreVideos():

	text = request.form['Texto']
	response = []

	doc = pln.TranslateSentence(text)
	frase = video.getTextoVideo(doc)

	response = make_response(jsonify(frase = frase))

	# doc = pln.TranslateSentence(text)
	# resultado = video.getTextoVideo(doc)


	# if (resultado['error'] == True):
	# 	raise BadRequest(resultado['resultado'], 404, { 'ext': 1 })
	# else:
	# 	frase = resultado['resultado']
	# 	response = make_response(jsonify(frase = frase))

	return response



if __name__ == '__main__':
    app.run(port=8080)