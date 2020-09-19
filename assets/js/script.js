// App initialization code goes here

import io from 'socket.io-client';

function connect_to_socketio(){
    var socket = io();
    socket.on('connect', function() {
        console.log('connected');
        socket.emit('my event', {data: 'I\'m connected!'});
    });
};

window.connect_to_socketio = connect_to_socketio;
