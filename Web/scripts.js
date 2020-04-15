
// ------------------------------------------------------------------------------------------------------------------------------------------
// --------------------------------------------------------------- FETCH --------------------------------------------------------------------
// ------------------------------------------------------------------------------------------------------------------------------------------

// Control de errores en las llamadas Fetch
function handleErrors(response){

	if(!response.ok) {
		console.log('Error handleErrors: ' + response.statusText);
	}
	return response;
}

// Llamada a TextoLSE POST - > Devuelve Json
function GetTextLSEJson(){

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

			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
			}
			else{
				return response.json();
			}
			
		})
	.then(function(text){ 
		$('#JSONText').html(text.texto.toUpperCase())
	})
	.catch(
		function(error){
			console.log(error);
		});

}

// Llamada a TextoLSEVideos POST- > Devuelve Json
function GetTextLSEVideosJson(){

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
				return response.text();
			}
			else{
				return response.json();
			}
			
		})
	.then(function(text){ 
		$('#JSONContainer').html(text.texto)
	})
	.catch(
		function(error){
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
			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
				return response.text();
				
			}
			else{
				var url = window.URL || window.webkitURL; 
				response.blob().then(function(video) {
					var objectUrl = url.createObjectURL(video);
					$('#videoContainer').html('<video id="video" width="300" height="240" controls><source id="source" src="' + objectUrl + '" type=video/mp4></video>');	
				})
			}
	})
	.then(function(body){
			$('#textoError').text(JSON.parse(body).message);
			$('#errorModal').modal('show');
			$('.loader').hide();
		}
	)
	.catch(
		function(error){
			console.log(error);
		});
}

// Llamada a /video POST -> Devuelve video
function GetVideoSentence(){
	$('#videoContainer video').remove();
	$("#videoContainer").html('<div class="loader center"></div>');
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

			if(response.status != 200)
			{
				console.log('Error: ' + response.status);
				return response.text();
				
			}
			else{
				var url = window.URL || window.webkitURL; 
				response.blob().then(function(video) {
					var objectUrl = url.createObjectURL(video);
					$('#videoContainer').html('<video id="video" class="embeb-responsive-item" autoplay controls><source id="source" src="' + objectUrl + '" type=video/mp4></video>');	
				})
			}
			
		})
	.then(function(body){
			$('#textoError').text(JSON.parse(body).message);
			$('.loader').hide();
			$('#errorModal').modal('show');
		}
	)
	.catch(
		function(error){
			console.log(error);
		});

}