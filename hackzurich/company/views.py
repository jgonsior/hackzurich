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
from hackzurich.challenge.models import Challenge, User_Challenge_Association, Company
from hackzurich.database import db
import babel


blueprint = Blueprint(
    "company_blueprint", __name__, url_prefix="/companies", static_folder="../static"
)


@blueprint.route("/<int:company_id>")
@login_required
def display(company_id):
    company = Company.query.filter_by(id=company_id).first()

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
        "companies/company.html",
        company=company,
        country_total_co2=float(country_total_co2),
        total_saved_co2=float(total_saved_co2),
    )
