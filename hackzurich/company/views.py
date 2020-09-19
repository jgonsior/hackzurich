# -*- coding: utf-8 -*-
"""Challenge views."""
from datetime import datetime, timedelta
import datetime as dt
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
from .models import Challenge, User_Challenge_Association, Company
from hackzurich.database import db
import babel


blueprint = Blueprint(
    "company_blueprint", __name__, url_prefix="/companies", static_folder="../static"
)


@blueprint.route("/<int:company_id>")
@login_required
def display(company_id):
    company = Company.query.filter_by(id=company_id).first()
    return render_template("companies/company.html", company=company)


@blueprint.route("/create_new/", methods=["GET", "POST"])
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


@blueprint.route("/mark_failed/<int:challenge_id>")
@login_required
def mark_failed(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()

    user_challenge_association = (
        User_Challenge_Association.query.filter_by(
            user_id=current_user.id, challenge_id=challenge.id
        )
        .order_by(User_Challenge_Association.commited_to_at.desc())
        .first()
    )
    user_challenge_association.done_at = dt.datetime.now()
    user_challenge_association.succeeded = False
    db.session.commit()

    flash(
        "You've aborted challenge "
        + str(challenge.challengename)
        + " "
        + str(user_challenge_association.id)
    )

    return redirect(url_for("challenge_blueprint.challenge", challenge_id=challenge_id))


@blueprint.route("/mark_done/<int:challenge_id>")
@login_required
def mark_done(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()

    user_challenge_association = (
        User_Challenge_Association.query.filter_by(
            user_id=current_user.id, challenge_id=challenge.id
        )
        .order_by(User_Challenge_Association.commited_to_at.desc())
        .first()
    )
    user_challenge_association.done_at = dt.datetime.now()
    user_challenge_association.succeeded = True
    db.session.commit()

    flash("You've successfully done challenge " + str(challenge.challengename))

    return redirect(url_for("challenge_blueprint.challenge", challenge_id=challenge_id))


@blueprint.route("/commit/<int:challenge_id>")
@login_required
def commit(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    user = current_user

    user_challenge_association = User_Challenge_Association.create(
        user_id=user.id, challenge_id=challenge.id
    )
    flash("You've successfully commited to challenge " + str(challenge.challengename))

    return redirect(url_for("challenge_blueprint.challenge", challenge_id=challenge_id))
