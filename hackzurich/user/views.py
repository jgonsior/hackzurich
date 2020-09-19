# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
from hackzurich.challenge.models import Challenge

blueprint = Blueprint("user_blueprint", __name__, url_prefix="/users", static_folder="../static")


@blueprint.route("/")
@login_required
def members():
    """List members."""
    # 1. get list of active challenges
    # display them
    active_challenges = Challenge.query.filter_by(active=True).all()
    return render_template("users/members.html", active_challenges=active_challenges)
