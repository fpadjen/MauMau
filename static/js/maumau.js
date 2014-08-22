$(document).ready(function() {
	// Open a WebSocket connection.
	var wsUri =
			"ws://localhost:5000/ws";
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
	websocket.onmessage =
			function(ev) {
				console.log(ev);
				$('#output-area').append('<div>' +
						ev.data + '</div>');
				
				var output =
						$('#output-wrap');
				var height =
						output[0].scrollHeight;
				output.scrollTop(height);
			};

	// Error
	websocket.onerror =
			function(ev) {
				alert('Error ' +
						ev.data);
			};

	function textInput(e) {
		if (e.which == 13) {
			websocket.send($('#message')[0].value);
			$('#message')[0].value = '';
			return false;
		}
	}
			
	$('#message').keypress(textInput);
});