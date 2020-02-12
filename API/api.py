#------------------- Librerías Python -------------------#
from flask import Flask, abort, jsonify, request, send_file, make_response, abort
from flask_cors import CORS
import spacy
import os
#------------------- Archivos lógica --------------------#
import video

app = Flask(__name__)
CORS(app)
nlp = spacy.load("es_core_news_md")

# Ruta física donde se generan los vídeos
pathVideoGenerated = '/home/tfg/Documentos/tfg/TFG-1920-Text2LSE/API/' # Ruta Álex y Sara

# ---------------------------------------------------------------------------------------------------------
# ------------------------------------ PROCESAMIENTO VIDEO DE UNA PALABRA ---------------------------------
# ---------------------------------------------------------------------------------------------------------

@app.route("/video/<string:palabra>", methods=["GET"])
def getVideoPalabra(palabra):
    if video.existeVideo(palabra):
        videoPalabra = video.getVideoPalabra(palabra)
        
    else: abort(404)

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
def getTranslateText():

	text = request.form['TextToTranslate']
	doc = nlp(text)
	size = len(text.split())
	
	if(size == 1):
		
		if video.existeVideo(text):
			videoPalabra = video.getVideoPalabra(text)

		else: 
			abort(404, { 'message' : 'No existe el video para la palabra solicitada' })

		response = make_response(send_file(videoPalabra.filename, mimetype='video/mp4'))
		response.headers['Content-Transfer-Enconding']='base64'

	elif(size > 1):
		
		videoName = video.getTextVideo(doc)

		if (videoName == "error"):
			abort(404, { 'message' : 'No existen videos para todas las palabras solicitadas' })
		else:
			response = make_response(send_file(videoName, mimetype='video/mp4'))
			response.headers['Content-Transfer-Enconding']='base64'
			os.remove(pathVideoGenerated + videoName)

	return response

# ---------------------------------------------------------------------------------------------------------
# -------------------------------------------- HANDLERS ---------------------------------------------------
# ---------------------------------------------------------------------------------------------------------

@app.errorhandler(400)
def BadRequest(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def InternalServerError(e):
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(port=8080)