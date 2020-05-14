
// Inicializamos el contenido de la web
$(document).ready(function () {
	$('#spinner').hide();
	$('#videoContainer').hide();
	$('#JSONContainer').hide();
	$('#imageContainer').hide();

	if ($("body").height() < $(window).height()){
		$("footer").css({"position":"relative", "bottom" : "0px"});
	}

	var _originalSize = $(window).width() + $(window).height()
    $(window).resize(function() {
        if ($(window).width() + $(window).height() != _originalSize) {
            console.log("keyboard active");
            $("footer").removeClass("fixed");
        } else {
            console.log("keyboard closed");
            $("footer").addClass("fixed");
        }
    });

});

//var ruta = 'http://127.0.0.1:8080/';
var ruta = 'https://holstein.fdi.ucm.es/tfg-text2lse/';

// ------------------------------------------------------------------------------------------------------------------------------------------
// 							CONTROL ERRORES
// ------------------------------------------------------------------------------------------------------------------------------------------

// Control de errores en las llamadas Fetch
function handleErrors(response){

	if(!response.ok) {
		console.log('Error handleErrors: ' + response.statusText);
	}
	return response;
}

//---------------------------------------------------------------------------------------------------------------------------------
// 										SELECTOR DE TRADUCTOR
//---------------------------------------------------------------------------------------------------------------------------------

function Translate (){
	var formato = $('#formato option:selected').text();

	// introducido texto

	$('#videoContainer').hide();
	$('#JSONContainer').hide();
	$('#imageContainer').hide();
	$('#spinner').show();

	if (formato == "Vídeo")
	{
		//GetVideoSentence();
		GetSentenceVideo();
	}
	else if (formato == "Texto")
	{
		GetTextLSEJson();
	} 
	else if (formato == "Imagen")
	{
		GetImageSentence();
	}
}


//---------------------------------------------------------------------------------------------------------------------------------
// 										TEXTO TRADUCIDO A TEXTO LSE
//---------------------------------------------------------------------------------------------------------------------------------

// Llamada a TextoLSE POST - > Devuelve Json
function GetTextLSEJson(){

	var text = $('#textToTranslate').val();
	var url_api = ruta + 'TextoLSE/';
	event.preventDefault();
	
	var data = new FormData();
	data.append("Texto", text)

	fetch(url_api, {
	  method: "POST",
	  mode:'cors',
	  body: data
	})
	.then(handleErrors)
	.then( 
		function(response){

			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
			}
			else{
				return response.json();
			}
			
		})
	.then(function(text){ 
		$('body').removeClass('disableGrey');
		$('#spinner').hide();
		$('#JSONContainer').show();
		$('#JSONText').html(text.texto.toUpperCase())
	})
	.catch(
		function(error){
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			console.log(error);
		});

}

//---------------------------------------------------------------------------------------------------------------------------------
// 										IMÁGENES 
//---------------------------------------------------------------------------------------------------------------------------------

// Llamada a textoImagen POST - > Devuelve Json con el texto traducido según las imágenes existentes
function GetImageSentence(){
	$('#imageContainer').html('');
	var text = $('#textToTranslate').val();
	var url_api = ruta + 'textoImagen/';
	event.preventDefault();
	
	var data = new FormData();
	data.append("Texto", text)

	fetch(url_api, {
	  method: "POST",
	  mode:'cors',
	  body: data
	})
	.then(handleErrors)
	.then( 
		function(response){

			if(response.status != 200)
			{
				return response.text();
			}
			else{
				return response.text();
			}
			
		})
	.then(function(body){

		var bodyJson = JSON.parse(body);

		if (bodyJson.hasOwnProperty('frase'))
		{
			getImagenes(bodyJson.frase);
			$('#imageContainer').show();
		}
		else{
			$('#textoError').text("Lo sentimos, las siguientes palabras no se encuentran en la base de datos de ARASAAC: " + JSON.parse(body).message);
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			$('#errorModal').modal('show');
		}
			
	})
	.catch(
		function(error){
			('#textoError').text("Lo sentimos, ha ocurrido un error. Vuelva a intentarlo en unos minutos.");
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			$('#errorModal').modal('show');
		});

	$('body').removeClass('disableGrey');
	$('#spinner').hide();
}

async function getImagenes(frase)
{	
	var url_api = ruta + 'imagen/';

	for (palabra of frase){
		//$('#imageContainer').append('<img class="imageLSE" src="' + url_api + palabra + '"/>');	
		$('#imageContainer').append('<figure class="wide"><img class="imageLSE" src="' + url_api + palabra + '"><figcaption><strong>' + palabra + '</strong></figcaption></figure>');
	}
}

//---------------------------------------------------------------------------------------------------------------------------------
// 								VIDEOS UNO DETRÁS DE OTRO EN CLIENTE
//---------------------------------------------------------------------------------------------------------------------------------

// Llamada a textoVideo POST -> Devuelve Json con el texto traducido según los videos existentes
function GetSentenceVideo(){

	var text = $('#textToTranslate').val();
	var url_api = ruta + 'TextoLSEVideos/';
	event.preventDefault();
	
	var data = new FormData();
	data.append("Texto", text)

	fetch(url_api, {
	  method: "POST",
	  mode:'cors',
	  body: data
	})
	.then(handleErrors)
	.then( 
		function(response){

			if(response.status != 200)
			{
				return response.text();
			}
			else{
				return response.text();
			}
			
		})
	.then(function(body){

		var bodyJson = JSON.parse(body);

		if (bodyJson.hasOwnProperty('frase'))
		{
			getVideos(bodyJson.frase);
			
		}
		else{
			$('#textoError').text("Lo sentimos, las siguientes palabras no se encuentran en la base de datos de ARASAAC: " + JSON.parse(body).message);
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			$('#errorModal').modal('show');
		}
			
	})
	.catch(
		function(error){
			('#textoError').text("Lo sentimos, ha ocurrido un error. Vuelva a intentarlo en unos minutos.");
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			$('#errorModal').modal('show');
		});

	$('body').removeClass('disableGrey');
	$('#spinner').hide();
}

// Funciones globales para video
	var vidSources = [];
	var nextVideo = "", fraseVideo = "";
	var nextActiveVideo = 0;
	var videoObjects = [
			$('#videoLSE1'),
			$('#videoLSE2')
		];

// Función que muestra los videos uno detrás de otro
async function getVideos(frase)
{	
	videoObjects = [
			$('#videoLSE1'),
			$('#videoLSE2')
		];
	fraseVideo = frase;
	
	var url_api = ruta + 'video/';
	nextActiveVideo = 0;
	vidSources = [];

	for (palabra of frase){
		vidSources.push(url_api + palabra);
	}

	videoObjects[0][0].inx = 0; 
	videoObjects[1][0].inx = 1;

	initVideoElement(videoObjects[0][0]);
	initVideoElement(videoObjects[1][0]);

	videoObjects[0][0].autoplay = true;
	videoObjects[0].attr("src", vidSources[nextActiveVideo]);
	$('#txtVideo').text(fraseVideo[nextActiveVideo]);
	$('#videoContainer').show();
}

function initVideoElement(video)
{
    video.playsinline = true;
    video.muted = false;
    video.preload = 'auto'; 

    video.onplaying= function()
    {
        nextActiveVideo = ++nextActiveVideo % vidSources.length;

        if(this.inx == 0){
            nextVideo = videoObjects[1][0];
        }
        else
            nextVideo = videoObjects[0][0];

        nextVideo.src = vidSources[nextActiveVideo];
        nextVideo.load();
        nextVideo.pause();
    };

    video.onended = function()
    {
        this.style.display = 'none';
        nextVideo.style.display = 'inline';
        $('#txtVideo').text(fraseVideo[nextActiveVideo]);
        if (nextActiveVideo != 0)
        {
        	nextVideo.play();
        }
        
    };
}

//---------------------------------------------------------------------------------------------------------------------------------
// 								VIDEOS JUNTOS EN SERVIDOR
//---------------------------------------------------------------------------------------------------------------------------------

// Llamada a /video POST -> Devuelve video
function GetVideoSentence(){
	$('#videoContainer video').remove();
	var text = $('#textToTranslate').val();
	var url_api = ruta + 'video/';
	event.preventDefault();

	var data = new FormData();
	data.append("Texto", text)

	fetch(url_api, {
	  method: "POST",
	  mode:'cors',
	  body: data
	})
	.then(handleErrors)
	.then( 
		function(response){

			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
				return response.text();
				
			}
			else{
				var url = window.URL || window.webkitURL; 
				response.blob().then(function(video) {
					var objectUrl = url.createObjectURL(video);
					$('body').removeClass('disableGrey');
					$('#spinner').hide();
					$('#videoContainer').show();
					$('#videoContainer').html('<video id="video" class="embeb-responsive-item" autoplay controls><source id="source" src="' + objectUrl + '" type=video/mp4></video>');	
				})
			}
			
		})
	.then(function(body){
			$('#textoError').text(JSON.parse(body).message);
			$('body').removeClass('disableGrey');
			$('#spinner').hide();
			$('#errorModal').modal('show');
		}
	)
	.catch(
		function(error){
			console.log(error);
		});

}