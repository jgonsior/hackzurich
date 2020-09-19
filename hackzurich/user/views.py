# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from hackzurich.challenge.models import Challenge, User_Challenge_Association
import csv

blueprint = Blueprint(
    "user_blueprint", __name__, url_prefix="/users", static_folder="../static"
)


@blueprint.route("/")
@login_required
def members():
    """List members."""
    active_challenges = Challenge.query.filter_by(active=True).all()
    done_user_challenges = User_Challenge_Association.query.filter_by(
        user_id=current_user.id, succeeded=True
    ).all()

    done_challenges = []
    total_saved_co2 = 0
    for done_user_challenge in done_user_challenges:
        done_user_challenge.challenge = Challenge.query.filter_by(
            id=done_user_challenge.challenge_id
        ).first()
        done_challenges.append(done_user_challenge)
        total_saved_co2 += done_user_challenge.challenge.co2offset

    for active_challenge in active_challenges:
        user_challenge_association = (
            User_Challenge_Association.query.filter_by(
                user_id=current_user.id, challenge_id=active_challenge.id
            )
            .order_by(User_Challenge_Association.commited_to_at.desc())
            .first()
        )
        active_challenge.user_challenge_association = user_challenge_association

        active_challenge.total_participants = (
            User_Challenge_Association.query.distinct(
                User_Challenge_Association.user_id
            )
            .filter_by(challenge_id=active_challenge.id)
            .count()
        )

    with open("co2data/co2clean.csv") as csvfile:
        reader = csv.reader(csvfile)
        country_co2_csv = {rows[0]: rows[1] for rows in reader}

    country_total_co2 = float(country_co2_csv[current_user.country])

    return render_template(
        "users/members.html",
        active_challenges=active_challenges,
        done_challenges=done_challenges,
        total_saved_co2=total_saved_co2,
        country_total_co2=country_total_co2,
    )
