#------------------- Librerías Python -------------------#
import os, uuid, pln

#------------------- Archivos lógica --------------------#
import constantes as const


def existeImagen(palabra):
	if(os.path.isfile(const.pathImagen + palabra.lower() +".jpg")):
		return True
	return False

def getImagenPalabra(palabra):
    return const.pathImagen + palabra.lower() +".jpg"

def getTextoImagenes(sentence):
	frase = []
	
	for palabra in sentence:
		if existeImagen(palabra.lower()):
			frase.append(palabra.lower())

		else:
			# tratar plurales y femeninos
			diccionario = pln.getDiccionarioOracion()
			if (pln.keyexits(palabra, diccionario)):
				values = pln.getKeyValue(palabra, diccionario)
				if(values.get("Pos") == "NOUN"):
					# buscamos el vídeo de la palabra en masculino singular
					if existeImagen(values.get("lemma")):
						frase.append(values.get("lemma").lower())

						# si la palabra era femenina añadir "mujer"
						if values.get("Gender") == "Fem":
							frase.append("femenino")

						# si la palabra era plural se añade "otro"
						if values.get("Number") == "Plur":
							frase.append("plural")
					else:
						frase.append(palabra)
					
					# si la palabra era plural añadir 'plural' (RECORDAR PONER EL VIDEO 'PLURAL' IGUAL QUE EL DE 'OTRO')
					# si no existe -> error
				else:
					frase.append(palabra)
					
			else:
				frase.append(palabra)
				

	return frase


def getImagenesTexto(sentence):
	imagenes = []
	for palabra in sentence:
		image = getImagenPalabra(palabra)
		fileName = os.path.basename(image)
		nameImage =  os.path.splitext(fileName)
		imagenes.append("https://holstein.fdi.ucm.es/tfg-text2lse/imagen/" + nameImage[0])
	
	return imagenes


