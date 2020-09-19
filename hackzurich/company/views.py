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
    return render_template("companies/company.html", company=company)
