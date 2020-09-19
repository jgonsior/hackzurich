# -*- coding: utf-8 -*-
"""Chat views."""


from flask_login import login_required, current_user

from flask_socketio import emit, join_room

from hackzurich.extensions import (
    socketio,
    db
)

# from .forms import ChallengeForm
from .models import ChatMessage
from ..challenge.models import Challenge


@socketio.on('join_room')
@login_required
def join_room_socketio(data):
    """Join room if challenge exists."""
    challenge = db.session.query(Challenge).get(data['challenge_id'])
    if challenge:
        chat_room = challenge.chat_room
        join_room(chat_room.room_id)
        history = chat_room.get_history()
        emit('join_room', {'history': history})


@socketio.on('send_message')
@login_required
def send_message(data):
    """A user wants to send a message to a chat room."""
    challenge = db.session.query(Challenge).get(data['challenge_id'])

    if challenge:
        chat_room = challenge.chat_room
        msg = ChatMessage.create(text=data['text'], user=current_user, room=chat_room)
        j = msg.get_json()

        emit('new_message', j)

        j['is_self'] = False
        emit('new_message', j, room=chat_room.room_id, include_self=False)
