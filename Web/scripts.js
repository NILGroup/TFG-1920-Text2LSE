
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
function SendText(){

	var text = $('#textToTranslate').val();
	var jSonText = {'TextToTranslate': text};

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