<h1 align="center">Api.py</h1>


## Signo de una palabra

Te permite obtener el signo de una palabra en concreto. 
* Método: ``GET``
* Response: ``.mp4``

```
http://127.0.0.1:8080/video/<palabra>
```

## Video de varias palabras

Te permite obtener un video con los signos de cada palabra del texto concatenados.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``.mp4``

```
http://127.0.0.1:8080/video/

```

## Json con la oración traducida a sordo

Te permite obtener un json con el texto traducido a sordo.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``json -> { "texto" : <frase traducida> } ``

```
http://127.0.0.1:8080/TextoLSE/

```

## Json con la oración traducida a sordo con el nombre de los videos que correspondan

Te permite obtener un json con el nombre de los videos que corresponden a la oración traducida a sordo.
* Método: ``POST``
* Json: ``{ 'Texto' : '<texto>'}``
* Response: ``json -> { "texto" : <frase traducida> } ``

```
http://127.0.0.1:8080/TextoLSEVideos/

```

## Autores ✒️

_Proyecto desarrollado por:_

* **Sara Vegas Cañas** - *Estudiante de Ing Informática UCM* 
* **Miguel Rodríguez Cuesta** - *Estudiante de Ing Informática UCM*
* **Alejandro Torralbo Fuentes** - *Estudiante de Ing Informática UCM*

_Proyecto dirigido por:_

* **Virginia Francisco Gilmartín**
* **Antonio García Sevilla** 


<h2>TRABAJO DE FIN DE GRADO 2019/2020 📌</h2> 

* GRADO DE INGENIERÍA INFORMÁTICA.
* Facultad de Informática.
* Universidad Complutense de Madrid.
* Convocatoria 2019/2020.
