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
				var data = JSON.parse(ev.data);
				$('#cards').empty();
				for (var i in data.player.hand) {
					var card = data.player.hand[i];
					$('#cards').append('<div class="col-md-1"><img src="/static/images/' + card +'.png" alt="bla"></div>');
				}
				
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
			return false;
		}
	}
			
	$('#message').keypress(textInput);
});