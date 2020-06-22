<h1 align="center">Text2LSE - API</h1>

Traducción a Video
===

## Signo de una palabra (Vídeo)

Te permite obtener el vídeo de un signo en concreto. 
* Método: ``GET``
* Response: ``.mp4``

```
https://holstein.fdi.ucm.es/tfg-text2lse/video/<palabra>
```

## Traducción en video de una oración

Te permite obtener un video con la traducción a LSE de una oración.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``.mp4``

```
https://holstein.fdi.ucm.es/tfg-text2lse/video/
```

## Traducción adaptada al catálogo de vídeos de ARASAAC
Te permite obtener un json con el nombre de los videos a reproducir adaptados a la biblioteca de ARASAAC. Desde el cliente se pueden obtener los videos con el servicio **Signo de una palabra (Vídeo)**.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``.json -> { "frase" : frase traducida }``

```
https://holstein.fdi.ucm.es/tfg-text2lse/TextoLSEVideos/
```

Traducción a Imagen
===
## Signo de una palabra (Imagen)

Te permite obtener la imagen de un signo en concreto. 
* Método: ``GET``
* Response: ``.jpeg``

```
https://holstein.fdi.ucm.es/tfg-text2lse/imagen/<palabra>
```
## Traducción en imagen de una oración
Te permite obtener un listado de imagenes que representan los signos de la frase a traducir.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``.json -> { "rutas" : [rutas de imágenes] }``
```
https://holstein.fdi.ucm.es/tfg-text2lse/imagenes/
```
## Traducción adaptada al catálogo de imágenes de ARASAAC
Te permite obtener un json con el nombre de las imágenes a reproducir adptadas a la biblioteca  de ARASAAC. Desde el cliente se pueden obtener estas imágenes con el servicio **Signo de una palabra (Imagen)**.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``.json -> { "frase" : <frase traducida> }``

```
https://holstein.fdi.ucm.es/tfg-text2lse/textoImagen/
```

Traducción a texto en LSE
===


## Json con la oración traducida a texto LSE

Te permite obtener un json con el texto traducido a texto LSE.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``json -> { "frase" : <frase traducida> } ``

```
https://holstein.fdi.ucm.es/tfg-text2lse/TextoLSE/
```


 Autores de Text2LSE  ✒️ 
===

_Proyecto desarrollado por:_

* **Sara Vegas Cañas** - *Estudiante de Ing Informática UCM* 
* **Miguel Rodríguez Cuesta** - *Estudiante de Ing Informática UCM*
* **Alejandro Torralbo Fuentes** - *Estudiante de Ing Informática UCM*

_Proyecto dirigido por:_

* **Virginia Francisco Gilmartín**
* **Antonio García Sevilla** 


TRABAJO DE FIN DE GRADO 2019/2020 📌
===

* GRADO DE INGENIERÍA INFORMÁTICA.
* Facultad de Informática.
* Universidad Complutense de Madrid.
* Convocatoria 2019/2020.
