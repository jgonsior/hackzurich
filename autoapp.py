# -*- coding: utf-8 -*-
"""Create an application instance."""
import click
from hackzurich.app import create_app
from hackzurich.extensions import socketio

app = create_app()

@app.cli.command("run-socketio")
def run_socketio():
    socketio.run(app)
