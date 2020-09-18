# -*- coding: utf-8 -*-
"""Challenge models."""
import datetime as dt

from flask_login import ChallengeMixin

from hackzurich.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)
from hackzurich.extensions import bcrypt


class Role(PkModel):
    """A role for a challenge."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    challenge_id = reference_col("challenges", nullable=True)
    challenge = relationship("Challenge", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class Challenge(ChallengeMixin, PkModel):
    """A challenge of the app."""

    __tablename__ = "challenges"
    challengename = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, challengename, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(challengename=challengename, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full challenge name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Challenge({self.challengename!r})>"
