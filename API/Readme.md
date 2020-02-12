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
* Response: ``.mp4``
* Json: ``{ 'TextToTranslate' : '<texto>'}``

```
http://127.0.0.1:8080/video/

```

## Autores ✒️

_Proyecto desarrollado por:_

* **Sara Vegas Cañas** - *Estudiante de Ing Informática UCM* 
* **Miguel Rodríguez Cuesta** - *Estudiante de Ing Informática UCM*
* **Alejandro Torralbo Torres** - *Estudiante de Ing Informática UCM*

_Proyecto dirigido por:_

* **Virginia Francisco Gilmartín**
* **Antonio García Sevilla** 


<h2>TRABAJO DE FIN DE GRADO 2019/2020 📌</h2> 

* GRADO DE INGENIERÍA INFORMÁTICA.
* Facultad de Informática.
* Universidad Complutense de Madrid.
* Convocatoria 2019/2020.