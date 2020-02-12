import os, uuid
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Ruta física de los vídeos
#path = "C:/Users/Miguel/Desktop/videos/" # Ruta Miguel
path = "/home/tfg/Escritorio/lse/videos/" # Ruta Álex y Sara

# Ruta física donde se generan los vídeos
pathVideoGenerated = '/home/tfg/Documentos/tfg/TFG-1920-Text2LSE/API/' # Ruta Álex y Sara


def existeVideo(token):
    #Se puede utilizar con el Texto ya que solo hay que
    #pasarle el token (bucle for).
    if(os.path.isfile(path + token +".mp4")):
        return True
    return False

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA ----------------------------------
# ------------------------------------------------------------------------------------------------------
def getVideoPalabra(palabra):
    return VideoFileClip(path + palabra +".mp4")

 
# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE VARIAS PALABRAS ------------------------------
# ------------------------------------------------------------------------------------------------------

# Comprobar que todos los videos de la frase están en la carpeta /videos 
# Si todos los videos existen -> Los mete en un array y los concatena, genera el video temporal y devuelve el nombre del video generado 
# Si no encuentra alguno de los videos -> Devuelve error
def getTextVideo(sentence):

	videos = []

	for token in sentence:
		if existeVideo(token.text):
			clip = VideoFileClip(path + token.text+  ".mp4")
			videos.append(clip)
		else:
			return "error"

	idVideo = str(uuid.uuid4())
	final_clip = concatenate_videoclips(videos)
	final_clip.write_videofile(pathVideoGenerated + idVideo + ".mp4")

	return idVideo + ".mp4"
