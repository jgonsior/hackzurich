// App initialization code goes here

import io from 'socket.io-client';

var socket = false;
function connect_to_socketio(challenge_id){
    socket = io('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('join_room', {'challenge_id': challenge_id});
    });

    return socket
};

window.connect_to_socketio = connect_to_socketio;
