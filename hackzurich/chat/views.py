# -*- coding: utf-8 -*-
"""Challenge views."""

# from hackzurich.utils import flash_errors
from flask import (
    # Blueprint,
    # render_template,
    # request,
    # flash,
    # redirect,
    # render_template,
    # url_for,
)

from flask_login import login_required

from flask_socketio import emit

from hackzurich.extensions import socketio

# from .forms import ChallengeForm
# from .models import Challenge

@socketio.on('connect')
@login_required
def test_connect():
    print('connected')
    emit('connection_successfull', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
