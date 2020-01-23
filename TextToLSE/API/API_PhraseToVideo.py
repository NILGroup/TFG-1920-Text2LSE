from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, make_response
from moviepy.editor import VideoFileClip, concatenate_videoclips

import os,uuid,spacy


app = Flask(__name__)
CORS(app)

app.config["videos"] = "videos/"


videos = []

@app.route("/PhraseToVideo/", methods=["POST"])
def videoProcessing():

    #Obtener el JSON con el texto
    if request.method == 'POST':
        content = request.get_json(force=True)
        if 'texto' in content.keys():
            text = content['texto']

    #Obtener el Doc para Tokenizar
    nlp = spacy.load("es")
    doc = nlp(text)

    #Obtener el video de cada token
    url_videos = "videos/"
    for token in doc:     
        if os.path.isfile(url_videos + token.text +".mp4"):
            print(token.text + " " +  "Found")
            clip = VideoFileClip("videos/" + token.text+  ".mp4")
            videos.append(clip)
            
            
        else:
            print(token.text + " " + "Not Found") 

    #Concatenacón del video y creación del video con uuid propio.
    idVideo = str(uuid.uuid4())
    final_clip = concatenate_videoclips(videos)
    final_clip.write_videofile(idVideo + " " + text + ".mp4", threads = 8, fps=24, audio=False, preset='ultrafast')

    response = make_response(send_file(idVideo + " " + text + ".mp4", mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'

    return response




if __name__ == '__main__':
    app.run(port=5000)