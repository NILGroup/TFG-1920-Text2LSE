from flask import Flask, jsonify, request
from flask_cors import CORS
from flask import send_file, send_from_directory, safe_join, abort, make_response
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os,uuid,spacy

app = Flask(__name__)
CORS(app)
app.config["videos"] = "videos/"

videoWord = 0

@app.route("/WordToVideo/", methods=["POST"])
def videoProcessing():

    videoWord = 0

    #Obtener el JSON con el texto
    if request.method == 'POST':
        content = request.get_json(force=True)
        if 'word' in content.keys():
            word = content['word']

   

    #Obtener el video de cada token
    url_videos = "videos/"
        
    if os.path.isfile(url_videos + word +".mp4"):
        print(word + " " +  "Found")
        videoWord = VideoFileClip("videos/" + word +  ".mp4")
        videoWord.write_videofile(word + ".mp4", threads = 8, fps=24, audio=False, preset='ultrafast')
        
        
    else:
        print(word + " " + "Not Found") 

    
    response = make_response(send_file(word + ".mp4", mimetype='video/mp4'))
    response.headers['Content-Transfer-Enconding']='base64'

    return response




if __name__ == '__main__':
    app.run(port=5000)