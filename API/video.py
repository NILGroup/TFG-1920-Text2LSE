#------------------- Librerías Python -------------------#
import os, uuid, pln
from moviepy.editor import VideoFileClip, concatenate_videoclips

#------------------- Archivos lógica --------------------#
import constantes as const


# Devuelve true si existe video para la palabra, false si error
def existeVideo(palabra):
    if(os.path.isfile(const.path + palabra.lower() +".mp4")):
        return True
    return False

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA ----------------------------------
# ------------------------------------------------------------------------------------------------------
def getVideoPalabra(palabra):
    return VideoFileClip(const.path + palabra.lower() +".mp4")

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE VARIAS PALABRAS ------------------------------
# ------------------------------------------------------------------------------------------------------

# Comprobar que todos los videos de la frase están en la carpeta /videos 
# Si todos los videos existen -> Los mete en un array y los concatena, genera el video temporal y devuelve el nombre del video generado 
# Si no encuentra alguno de los videos -> Devuelve error
def getTextoVideo(sentence):

	videos = []
	errores = ''
	correcto = True

	resultado = {'error': False, 'resultado':''}

	for palabra in sentence:
		if existeVideo(palabra.lower()):
			clip = VideoFileClip(const.path + palabra.lower() + ".mp4")
			videos.append(clip)
		else:
			# tratar plurales y femeninos
			diccionario = pln.getDiccionarioOracion()
			if (pln.keyexits(palabra, diccionario)):
				values = pln.getKeyValue(palabra, diccionario)
				if(values.get("Pos") == "NOUN"):
					# buscamos el vídeo de la palabra en masculino singular
					if existeVideo(values.get("lemma")):
						clip = VideoFileClip(const.path + values.get("lemma").lower() + ".mp4")
						videos.append(clip)

						# si la palabra era femenina añadir "mujer"
						if values.get("Gender") == "Fem":
							clip = VideoFileClip(const.path + "mujer" + ".mp4")
							videos.append(clip)

						# si la palabra era plural se añade "otro"
						if values.get("Number") == "Plur":
							clip = VideoFileClip(const.path + "otro" + ".mp4")
							videos.append(clip)
					
					# si la palabra era plural añadir 'plural' (RECORDAR PONER EL VIDEO 'PLURAL' IGUAL QUE EL DE 'OTRO')
					# si no existe -> error
				else:
					correcto = False
			else:
				correcto = False
			

			if errores == '':
				errores = '\'' + palabra.lower() + '\''
			else:
				errores = errores + ', \'' + palabra.lower() + '\''
			
	if correcto:
		
		idVideo = str(uuid.uuid4())
		final_clip = concatenate_videoclips(videos, method="compose")
		#final_clip.write_videofile(const.pathVideoGenerado + idVideo + ".mp4")
		final_clip.write_videofile(const.pathVideoGenerado + idVideo + ".mp4", threads=6, audio=False, preset='ultrafast')
	
		resultado['resultado'] = idVideo + ".mp4"

	else:
		resultado['resultado'] = errores
		resultado['error'] = True

	return resultado
