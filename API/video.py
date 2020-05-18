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

# # Agrega un error a una lista de errores
# def agregaErrores (errores, palabra):
# 	if errores == '':
# 		errores = '\'' + palabra.lower() + '\''
# 	else:
# 		errores = errores + ', \'' + palabra.lower() + '\''

# 	return errores

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE UNA PALABRA ----------------------------------
# ------------------------------------------------------------------------------------------------------
def getVideoPalabra(palabra):
	return VideoFileClip(const.path + palabra.lower() +".mp4")
	

# ------------------------------------------------------------------------------------------------------
# -------------------------------- PROCESAMIENTO VIDEO DE VARIAS PALABRAS ------------------------------
# ------------------------------------------------------------------------------------------------------
def getTextoVideo(sentence):
    
	frase = []

	for palabra in sentence:
		if existeVideo(palabra.lower()):
			frase.append(palabra.lower())
		else:
			# tratar plurales y femeninos
			diccionario = pln.getDiccionarioOracion()
			if (pln.keyexits(palabra, diccionario)):
				values = pln.getKeyValue(palabra, diccionario)
				if(values.get("Pos") == "NOUN"):
					# buscamos el vídeo de la palabra en masculino singular
					if existeVideo(values.get("lemma")):
						frase.append(values.get("lemma").lower())

						# si la palabra era femenina añadir "mujer"
						if values.get("Gender") == "Fem":
							frase.append("mujer")

						# si la palabra era plural se añade "otro"
						if values.get("Number") == "Plur":
							frase.append("otro")
					else: frase.append(palabra)
					# si la palabra era plural añadir 'plural' (RECORDAR PONER EL VIDEO 'PLURAL' IGUAL QUE EL DE 'OTRO')
					# si no existe -> error
				else:
					frase.append(palabra)
					
			else:
				frase.append(palabra)


	return frase

#---------------
# def getTextoVideo(sentence):

# 	frase = []
# 	errores = ''
# 	correcto = True
# 	resultado = {'error': False, 'resultado':''}

# 	for palabra in sentence:
# 		if existeVideo(palabra.lower()):
# 			frase.append(palabra.lower())
# 		else:
# 			# tratar plurales y femeninos
# 			diccionario = pln.getDiccionarioOracion()
# 			if (pln.keyexits(palabra, diccionario)):
# 				values = pln.getKeyValue(palabra, diccionario)
# 				if(values.get("Pos") == "NOUN"):
# 					# buscamos el vídeo de la palabra en masculino singular
# 					if existeVideo(values.get("lemma")):
# 						frase.append(values.get("lemma").lower())

# 						# si la palabra era femenina añadir "mujer"
# 						if values.get("Gender") == "Fem":
# 							frase.append("mujer")

# 						# si la palabra era plural se añade "otro"
# 						if values.get("Number") == "Plur":
# 							frase.append("otro")
					
# 					# si la palabra era plural añadir 'plural' (RECORDAR PONER EL VIDEO 'PLURAL' IGUAL QUE EL DE 'OTRO')
# 					# si no existe -> error
# 				else:
# 					correcto = False
# 					errores = agregaErrores(errores, palabra)
# 			else:
# 				correcto = False
# 				errores = agregaErrores(errores, palabra)

# 	if correcto:
# 		resultado['resultado'] = frase

# 	else:
# 		resultado['resultado'] = errores
# 		resultado['error'] = True

# 	return resultado

def getVideoTexto(sentence):

	videos = []
	
	for palabra in sentence:
		clip = VideoFileClip(const.path + palabra.lower() + ".mp4")
		videos.append(clip)
		
			
	
		idVideo = str(uuid.uuid4())
		final_clip = concatenate_videoclips(videos, method="compose")
		final_clip.write_videofile(const.pathVideoGenerado + idVideo + ".mp4", threads=6, audio=False, preset='ultrafast')

	return idVideo + ".mp4"