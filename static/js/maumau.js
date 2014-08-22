$(document).ready(function() {
	// Open a WebSocket connection.
	var wsUri =
			'ws://' + window.location.host + '/ws';
	websocket =
			new WebSocket(wsUri);

	// Connected to server
	websocket.onopen =
			function(ev) {
				console.log('Connected to server ');
			};

	// Connection close
	websocket.onclose =
			function(ev) {
				console.log('Disconnected: ' + ev);
			};

	// Message Receved
	function add_message(message) {
		$('#output-area').append('<div>' +
				message + '</div>');
		
		var output =
				$('#output-wrap');
		var height =
				output[0].scrollHeight;
		output.scrollTop(height);
	}
			
	websocket.onmessage =
			function(ev) {
				add_message(ev.data);
			};

	// Error
	websocket.onerror =
			function(ev) {
				alert('Error ' +
						ev.data);
			};

	function textInput(e) {
		if (e.which == 13) {
			var message = $('#message')[0].value;
			websocket.send(message);
			$('#message')[0].value = '';
			add_message(message);
			return false;
		}
	}
			
	$('#message').keypress(textInput);
});