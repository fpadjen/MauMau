$(document).ready(function() {
	// Open a WebSocket connection.
	var wsUri =
			"ws://localhost:5000/ws";
	websocket =
			new WebSocket(wsUri);

	// Connected to server
	websocket.onopen =
			function(ev) {
				// alert('Connected to server ');
			};

	// Connection close
	websocket.onclose =
			function(ev) {
				alert('Disconnected');
			};

	// Message Receved
	websocket.onmessage =
			function(ev) {
				$('#output-area').append('<div>' +
						ev.data + '</div>');
				$('#message')[0].value =
						'';
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

	$('#message').keypress(function(e) {
		if (e.which == 13) {
			websocket.send($('#message')[0].value);
			return false;
		}
	});
});