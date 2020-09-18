# -*- coding: utf-8 -*-
"""Challenge forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import Challenge


class RegisterForm(FlaskForm):
    """Register form."""

    challengename = StringField(
        "Challengename", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.challenge = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        challenge = Challenge.query.filter_by(
            challengename=self.challengename.data
        ).first()
        if challenge:
            self.challengename.errors.append("Challengename already registered")
            return False
        challenge = Challenge.query.filter_by(email=self.email.data).first()
        if challenge:
            self.email.errors.append("Email already registered")
            return False
        return True
