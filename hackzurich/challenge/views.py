# -*- coding: utf-8 -*-
"""Challenge views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    "challenge", __name__, url_prefix="/challenges", static_folder="../static"
)


@blueprint.route("/<int:challenge_id>")
@login_required
def challenge(challenge_id):
    print(challenge_id)
    """List members."""
    return render_template("challenges/challenges.html", challenge_id=challenge_id)
