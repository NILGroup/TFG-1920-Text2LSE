// ------------------------------------------------------------------------------------------------------------------------------------------
// --------------------------------------------------------------- AJAX ---------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------

//FUNCIONA PARA ENVIAR y RECIBIR TEXTO
function SendTextAnterior(){
	var text = $('#textToTranslate').val();
	var jSonText = {'textToTranslate': text};
	event.preventDefault();

	$.ajax({
		type: "POST",
		url: "http://127.0.0.1:5000/TranslateText/",
		data: jSonText,
		success: function(response){
			alert('entra');
			$('#spanFinal').html("<p>Texto: " + response[0].text);
			console.log(response[1].text);
		},
		error: function(error) {
			console.log(error);
		},
		dataType: "JSON"

	});
}


//FUNCIONAAA para imagenes arasaac (SOLO GET)
function SendTextIMAGEN(){

	event.preventDefault();

	$.ajax({ 
		
		url:'https://api.arasaac.org/api/pictograms/4665?backgroundColor=%23CCC&plural=true&action=past&skin=black',
		cache:false, 
		xhr:function(){// Seems like the only way to get access to the xhr object 
			var xhr = new XMLHttpRequest(); 
			xhr.responseType= 'blob' 
			return xhr; 
		}, 
		success: function(data){ 
			console.log(data);
  			alert('entra');
			var img = document.getElementById('img'); 
			var url = window.URL || window.webkitURL; 
			img.src = url.createObjectURL(data); }, 
		error:function(data){
			console.log(data);
			alert('eeeerror');
	 	} 
	});
}


//FUNCIONA DEFINITIVO 100% VIDEO POR POST
function SendTextAJAX(){

	var text = $('#textToTranslate').val();
	var jSonText = {'Texto': text};

	event.preventDefault();

	$.ajax({ 
		type: 'POST',
		url:'http://127.0.0.1:5000/TranslateText/',
		data: jSonText,
		cache:false, 
		xhr:function(){ 
			var xhr = new XMLHttpRequest(); 
			xhr.responseType= 'blob' 
			return xhr; 
		}, 
		success: function(data){
		debugger; 
			console.log(data);
  			alert('Success en ajax!');
			var url = window.URL || window.webkitURL; 
			$('#videoContainer').html('<video id="video" width="300" height="240" controls><source id="source" src="' + url.createObjectURL(data) + '" type=video/mp4></video>');
		},
		error:function(data){
			console.log(data);
			alert('error en ajax :(');
	 	} 
	});
}

// ------------------------------------------------------------------------------------------------------------------------------------------
// --------------------------------------------------------------- FETCH --------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------

// Control de errores en las llamadas Fetch
function handleErrors(response){
	debugger;
	if(!response.ok) {
		console.log('Error handleErrors: ' + response.statusText);
	}
	return response;
}

// Llamada a TextoLSE POST - > Devuelve Json
function GetTextLSEJson(){
	debugger;
	var text = $('#textToTranslateJSON').val();
	var url_api = 'http://127.0.0.1:8080/TextoLSE/';
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
			debugger;
			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
				// Mostrar error
			}
			else{
				return response.json();
			}
			
		})
	.then(function(text){ 
		$('#JSONText').html(text.texto)
		//alert(text.texto);
		// Hacer lo que se tenga que hacer con el texto.
	})
	.catch(
		function(error){
			// Mostrar error
			console.log(error);
		});

}

// Llamada a TextoLSEVideos POST- > Devuelve Json
function GetTextLSEVideosJson(){
	debugger;
	var text = $('#textToTranslate').val();
	var url_api = 'http://127.0.0.1:8080/TextoLSEVideos/';
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
				// Mostrar error
			}
			else{
				return response.json();
			}
			
		})
	.then(function(text){ 
		$('#JSONContainer').html(text.texto)
		//alert(text.texto);
		// Hacer lo que se tenga que hacer con el texto.
	})
	.catch(
		function(error){
			// Mostrar error
			console.log(error);
		});

}

// Llamada a /video/<palabra> GET -> Devuelve video
function GetVideoWord(){

	var text = $('#textToTranslate').val();
	var url_api = 'http://127.0.0.1:8080/video/' + text;
	event.preventDefault();

	fetch(url_api, {
	  mode:'cors'
	})
	.then(handleErrors)
	.then( 
		function(response){
			var url = window.URL || window.webkitURL; 
			response.blob().then(function(video) {
				var objectUrl = url.createObjectURL(video);
				$('#videoContainer').html('<video id="video" width="300" height="240" controls><source id="source" src="' + objectUrl + '" type=video/mp4></video>');	
			})
	})
	.catch(
		function(error){
			// Mostrar error

		});
}

// Llamada a /video POST -> Devuelve video
function GetVideoSentence(){
	debugger;
	var text = $('#textToTranslateVideo').val();
	var url_api = 'http://127.0.0.1:8080/video/';
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
			debugger;
			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
				// Mostrar error
			}
			else{
				var url = window.URL || window.webkitURL; 
				response.blob().then(function(video) {
				var objectUrl = url.createObjectURL(video);
				$('#videoContainer').html('<video id="video" class="embeb-responsive-item" autoplay controls><source id="source" src="' + objectUrl + '" type=video/mp4></video>');	
			})
			}
			
		})
	.catch(
		function(error){
			// Mostrar error
			console.log(error);
		});

}


// ---------------------------------- PENDIENTE ------------------------------------
// 1. Control de errores en las llamadas -> mostrarlos correctamente.
// 2. Poner spinner para que el usuario sepa que se está cargando.