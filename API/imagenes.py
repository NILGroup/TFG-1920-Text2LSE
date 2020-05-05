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

def agregaErrores (errores, palabra):
	if errores == '':
		errores = '\'' + palabra.lower() + '\''
	else:
		errores = errores + ', \'' + palabra.lower() + '\''

	return errores

def getTextoImagenes(sentence):
	frase = []
	errores = ''
	correcto = True
	resultado = {'error': False, 'resultado':''}

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
							frase.append("mujer")

						# si la palabra era plural se añade "otro"
						if values.get("Number") == "Plur":
							frase.append("otro")
					
					# si la palabra era plural añadir 'plural' (RECORDAR PONER EL VIDEO 'PLURAL' IGUAL QUE EL DE 'OTRO')
					# si no existe -> error
				else:
					correcto = False
					errores = agregaErrores(errores, palabra)
					
			else:
				correcto = False
				errores = agregaErrores(errores, palabra)
				
			
			
			
	if correcto:
		resultado['resultado'] = frase

	else:
		resultado['resultado'] = errores
		resultado['error'] = True

	return resultado

			
