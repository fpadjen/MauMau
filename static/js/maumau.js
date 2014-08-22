$(document).ready(function() {
	// Open a WebSocket connection.
	var wsUri =
			"ws://localhost:5000/ws";
	websocket =
			new WebSocket(wsUri);

	// Connected to server
	websocket.onopen =
			function(ev) {
//				alert('Connected to server ');
			}

	// Connection close
	websocket.onclose =
			function(ev) {
				alert('Disconnected');
			};

	// Message Receved
	websocket.onmessage =
			function(ev) {
				alert('Message ' +
						ev.data);
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