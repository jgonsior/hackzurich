# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, login_user, logout_user
import csv
from hackzurich.extensions import login_manager
from hackzurich.public.forms import LoginForm
from hackzurich.user.forms import RegisterForm
from hackzurich.user.models import User
from hackzurich.utils import flash_errors

blueprint = Blueprint("public_blueprint", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user_blueprint.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public_blueprint.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""

    with open("co2data/co2clean.csv") as csvfile:
        reader = csv.reader(csvfile)
        countries = [rows[0] for rows in reader]

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
            country=form.country.data,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public_blueprint.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form, countries=countries)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)
