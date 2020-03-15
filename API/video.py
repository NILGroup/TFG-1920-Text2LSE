#------------------- Librerías Python -------------------#
import os, uuid
from moviepy.editor import VideoFileClip, concatenate_videoclips
#------------------- Archivos lógica --------------------#
import constantes as const


# Devuelve true si existe video para la palabra, false si error
def existeVideo(palabra):
    if(os.path.isfile(const.path + palabra +".mp4")):
        return True
    return False

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA ----------------------------------
# ------------------------------------------------------------------------------------------------------
def getVideoPalabra(palabra):
    return VideoFileClip(const.path + palabra +".mp4")

 
# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE VARIAS PALABRAS ------------------------------
# ------------------------------------------------------------------------------------------------------

# Comprobar que todos los videos de la frase están en la carpeta /videos 
# Si todos los videos existen -> Los mete en un array y los concatena, genera el video temporal y devuelve el nombre del video generado 
# Si no encuentra alguno de los videos -> Devuelve error
def getTextoVideo(sentence):

	videos = []

	for palabra in sentence:
		if existeVideo(palabra):
			clip = VideoFileClip(const.path + palabra + ".mp4")
			videos.append(clip)
		else:
			return "error"

	idVideo = str(uuid.uuid4())
	final_clip = concatenate_videoclips(videos)
	final_clip.write_videofile(const.pathVideoGenerado + idVideo + ".mp4")

	return idVideo + ".mp4"
