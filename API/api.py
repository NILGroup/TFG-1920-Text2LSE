#------------------- Librerías Python -------------------#
from flask import Flask, abort, jsonify, request, send_file, make_response, abort
from moviepy.editor import VideoFileClip, concatenate_videoclips
#------------------- Archivos lógica --------------------#
import video

app = Flask(__name__)

@app.route("/video/<string:palabra>", methods=["GET"])
def getVideoPalabra(palabra):
    if video.existeVideo(palabra):
        videoPalabra = video.getVideoPalabra(palabra)
        
    else: abort(404)

    response = make_response(send_file(videoPalabra.filename, mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'
    
    return response




#--------------------------------------------------#
#----------------- HANDLERS -----------------------#
#--------------------------------------------------#
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