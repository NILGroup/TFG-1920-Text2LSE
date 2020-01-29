from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, make_response
from moviepy.editor import VideoFileClip, concatenate_videoclips

import os,uuid,spacy, shutil

app = Flask(__name__)
CORS(app)

app.config["videos"] = "videos/"

#URL donde se encuentran todos los videos
url = "videos/"


#Comprobar que el video está en la Carpeta /videos 
#y devuelve el video si lo encuentra.
def checkingWordVideo(url,filename):
    if os.path.isfile(url + filename +".mp4"):
        print(filename + " " +  "Found")
        videoWord = VideoFileClip(url + filename +".mp4")
        
    else:
        print(filename + " " + "Not Found") 
       
    return videoWord

#Comprobar que los videos están en la Carpeta /videos 
#y devuelve un array videos con todos los videos.
def checkingTextVideo(url,doc):

    videos = []
    for token in doc:     
        if os.path.isfile(url + token.text +".mp4"):
            print(token.text + " " +  "Found")
            clip = VideoFileClip("videos/" + token.text+  ".mp4")
            videos.append(clip)
            
            
        else:
            print(token.text + " " + "Not Found") 

    return videos


@app.route("/WordToVideo/", methods=["POST"])
def videoWordProcessing():

    #Obtener el JSON con la palabra que queremos procesar en video
    if request.method == 'POST':
        content = request.get_json(force=True)
        if 'word' in content.keys():
            word = content['word']

    final_clip = checkingWordVideo(url,word)

    idVideo = str(uuid.uuid4())
    final_clip.write_videofile(idVideo + word + ".mp4", threads = 8, fps=24, audio=False, preset='ultrafast')



    response = make_response(send_file(idVideo + word + ".mp4", mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'


    return response


@app.route("/PhraseToVideo/", methods=["POST"])
def videoTextProcessing():

    #Obtener el JSON con el texto
    if request.method == 'POST':
        content = request.get_json(force=True)
        if 'texto' in content.keys():
            text = content['texto']

    #Obtener el Doc para Tokenizar
    nlp = spacy.load("es")
    doc = nlp(text)

    videos = checkingTextVideo(url,doc)

    #Concatenación del video y creación del nuevo video con uuid propio.
    idVideo = str(uuid.uuid4())
    final_clip = concatenate_videoclips(videos)
    final_clip.write_videofile(idVideo + " " + text + ".mp4", threads = 8, fps=24, audio=False, preset='ultrafast')

    response = make_response(send_file(idVideo + " " + text + ".mp4", mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'

    return response




if __name__ == '__main__':
    app.run(port=5000)