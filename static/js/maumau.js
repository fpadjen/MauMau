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
		$('#output-area').prepend('<div>' +
				message + '</div>');
		$('#output-wrap').scrollTop(0);
	}
			
	function select_card(e) {
		websocket.send(e.target.alt);
	}
	
	websocket.onmessage =
			function(ev) {
				var data = JSON.parse(ev.data);
				
				if (data.we) {
					add_message(ev.data);
					$('#cards').empty();
					for (var i in data.player.hand) {
						var card = data.player.hand[i];
						if (data.player.playable_cards.indexOf(parseInt(i)) > -1) {
							$('#cards').append('<div class="col-md-1 playable"><img class="playercard" src="/static/images/' + card +'.png" alt="' + i + '"></div>');
						} else {
							$('#cards').append('<div class="col-md-1 unplayable"><img class="playercard" src="/static/images/' + card +'.png" alt="' + i + '"></div>');
						}
					}
					$('.playable').click(select_card);
				} else {
					if (data.action == 'play') {
						$('#' + data.player).remove();
						var element = '<div id="' + data.player + '">';
						element += '<div>' + data.player + '</div>';
						element += '<div class="row cards"></div>';
						element += '<div>' + data.action + '</div>';
						element += '<img class="othercard" src="/static/images/' + data.middle + '.png" alt="middle">';
						$('#players').append(element);
						var cards = $('#' + data.player).find(".cards");
						for (var j=0; j < data.number_of_cards; j++) {
							cards.append('<img class="othercard" src="/static/images/back.png" alt="' + j + '">');
						}
					} else {
						add_message(ev.data);
					}
				}
				
				$('#middle').empty();
				$('#middle').append('<div class="col-md-1 playable"><img class="playercard" src="/static/images/' + data.middle +'.png" alt="middle"></div>');
				
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