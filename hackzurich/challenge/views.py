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
from flask_login import login_required, current_user
from .forms import ChallengeForm
from .models import Challenge

blueprint = Blueprint(
    "challenge_blueprint", __name__, url_prefix="/challenges", static_folder="../static"
)


@blueprint.route("/<int:challenge_id>")
@login_required
def challenge(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
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


@blueprint.route("/mark_done/<int:challenge_id>")
@login_required
def mark_done(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    return render_template("challenges/challenges.html", challenge=challenge)


@blueprint.route("/commit/<int:challenge_id>")
@login_required
def commit(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    user = current_user
    print(user)
    return render_template("challenges/challenges.html", challenge=challenge)
