# -*- coding: utf-8 -*-
"""Challenge views."""
from hackzurich.utils import flash_errors
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required
from .forms import ChallengeForm
from .models import Challenge

blueprint = Blueprint(
    "challenge", __name__, url_prefix="/challenges", static_folder="../static"
)


@blueprint.route("/<int:challenge_id>")
@login_required
def challenge(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    """List members."""
    return render_template("challenges/challenges.html", challenge=challenge)


@blueprint.route("/create_new", methods=["GET", "POST"])
@login_required
def create_new():
    form = ChallengeForm(request.form)
    if form.validate_on_submit():
        Challenge.create(
            challengename=form.challengename.data,
            description=form.description.data,
            active=form.active.data,
        )
        flash("You've successfully created challenge ", str(form.challengename.data))
        return redirect(url_for("user.members"))
    else:
        flash_errors(form)
    return render_template("challenges/create_new.html", form=form)
