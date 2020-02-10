from flask import Flask, jsonify, redirect, url_for, request, Response, json
from flask import render_template
from flask_cors import CORS
from flask import abort, send_file, send_from_directory, safe_join, abort, make_response
from moviepy.editor import VideoFileClip, concatenate_videoclips

import spacy
import os
import uuid
import shutil


nlp = spacy.load("es_core_news_md")
doc = nlp("Yo como patatas")

app = Flask(__name__)
CORS(app)

app.config["videos"] = "videos/"


url = "videos/"



# ----------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA --------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------

# Comprobar que el video está en la carpeta /videos 
# Si el video existe -> Genera el video temporal y devuelve el nombre del video generado
# Si no lo encuentra -> Devuelve error
def getWordVideo(filename):

    if os.path.isfile(url + filename +".mp4"):

        final_clip = VideoFileClip(url + filename +".mp4")
        idVideo = str(uuid.uuid4())
        final_clip.write_videofile(idVideo + ".mp4", threads = 8, fps=24, audio=False, preset='ultrafast')

    else:
        return 404

    return idVideo + ".mp4"

       
