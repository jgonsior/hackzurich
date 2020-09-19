# -*- coding: utf-8 -*-
"""Challenge views."""
import csv
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
from hackzurich.user.models import User
from hackzurich.database import db
import babel
from hackzurich.chat.models import ChatRoom, ChatMessage


blueprint = Blueprint(
    "challenge_blueprint", __name__, url_prefix="/challenges", static_folder="../static"
)


@blueprint.route("/<int:challenge_id>")
@login_required
def challenge(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    company = Company.query.filter_by(id=challenge.company_id).first()
    challenge.company = company

    user_challenge_association = (
        User_Challenge_Association.query.filter_by(
            user_id=current_user.id, challenge_id=challenge.id, done_at=None
        )
        .order_by(User_Challenge_Association.commited_to_at.asc())
        .first()
    )

    streak = (
        User_Challenge_Association.query.filter_by(
            user_id=current_user.id, challenge_id=challenge.id, succeeded=True
        )
        .order_by(User_Challenge_Association.commited_to_at.desc())
        .all()
    )

    if len(streak) > 1:
        # cut off streak
        cut_off_date = datetime(*streak[0].done_at.timetuple()[:3])
        for user_challenge_association_streak in streak[1:]:
            if (
                datetime(*user_challenge_association_streak.done_at.timetuple()[:3])
                + timedelta(days=1)
                == cut_off_date
            ):
                cut_off_date = datetime(
                    *user_challenge_association_streak.done_at.timetuple()[:3]
                )
            elif (
                datetime(*user_challenge_association_streak.done_at.timetuple()[:3])
                == cut_off_date
            ):
                cut_off_date = datetime(
                    *user_challenge_association_streak.done_at.timetuple()[:3]
                )

            else:
                break

        streak = [s for s in streak if s.done_at > cut_off_date]

    total_co2offset = (
        User_Challenge_Association.query.filter_by(challenge_id=challenge.id).count()
        * challenge.co2offset
    )

    co2offset_by_you = (
        User_Challenge_Association.query.filter_by(
            challenge_id=challenge.id, user_id=current_user.id
        ).count()
        * challenge.co2offset
    )

    with open("co2data/co2clean.csv") as csvfile:
        reader = csv.reader(csvfile)
        country_co2_csv = {rows[0]: rows[1] for rows in reader}

    country_total_co2 = country_co2_csv[current_user.country]

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

    return render_template(
        "challenges/challenges.html",
        challenge=challenge,
        user_challenge_association=user_challenge_association,
        streak=streak,
        done_challenges=done_challenges,
        total_co2offset=total_co2offset,
        total_saved_co2=float(total_saved_co2),
        co2offset_by_you=co2offset_by_you,
        country_total_co2=float(country_total_co2),
    )


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
        return redirect(url_for("user_blueprint.members"))
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

    # notify chat about success
    admin = User.query.filter_by(id=1).first()
    chat_room = ChatRoom.query.filter_by(room_id=challenge.challengename).first()
    chat_message = ChatMessage.create(
        user=admin,
        text="Congrats! "
        + current_user.username
        + " has successfully solved this challenge!",
        room=chat_room,
    )
    #  datetime(*user_challenge_association_streak.done_at.timetuple()[:3])
    # check if it has been done five times today
    count_challenges_solved_today = (
        User_Challenge_Association.query.filter_by(challenge_id=challenge.id)
        .filter(
            User_Challenge_Association.commited_to_at
            <= datetime(*datetime.now().timetuple()[:3])
        )
        .filter(User_Challenge_Association.done_at != None)
        .count()
    )

    if count_challenges_solved_today % 5==0:
        company = Company.query.filter_by(id=challenge.company_id).first()
        chat_message = ChatMessage.create(
            user=admin,
            text="It has been solved "
            + str(count_challenges_solved_today)
            + " times so far! That means "
            + str(company.name)
            + " is doubling the amount of saved CO2 by this challenge for today!",
            room=chat_room,
        )

    return redirect(url_for("challenge_blueprint.challenge", challenge_id=challenge_id))


@blueprint.route("/commit/<int:challenge_id>")
@login_required
def commit(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    user = current_user

    user_challenge_association = User_Challenge_Association.create(
        user_id=user.id, challenge_id=challenge.id
    )

    # notify chat about success
    admin = User.query.filter_by(id=1).first()
    chat_room = ChatRoom.query.filter_by(room_id=challenge.challengename).first()
    chat_message = ChatMessage.create(
        user=admin,
        text=current_user.username + " has committed to this challenge. Good luck!",
        room=chat_room,
    )

    return redirect(url_for("challenge_blueprint.challenge", challenge_id=challenge_id))
