# -*- coding: utf-8 -*-
"""Challenge forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import Challenge


class ChallengeForm(FlaskForm):

    challengename = StringField(
        "Challenge Name", validators=[DataRequired(), Length(min=3, max=25)]
    )
    description = TextAreaField(
        "Description", validators=[DataRequired(), Length(min=6)]
    )
    active = BooleanField("Active?")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.challenge = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(ChallengeForm, self).validate()
        if not initial_validation:
            return False
        challenge = Challenge.query.filter_by(
            challengename=self.challengename.data
        ).first()
        if challenge:
            self.challengename.errors.append("Challengename already registered")
            return False
        return True
