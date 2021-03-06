# -*- coding: utf-8 -*-
"""Challenge models."""
import datetime as dt


from hackzurich.database import (
    Column,
    PkModel,
    db,
    reference_col,
    relationship,
)
from hackzurich.extensions import bcrypt


class Company(PkModel):
    __tablename__ = "company"

    name = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(500), nullable=True)
    challenges = relationship("Challenge", backref="company")

    def __init__(self, name, description, **kwargs):
        """Create instance."""
        super().__init__(name=name, description=description, **kwargs)


class User_Challenge_Association(PkModel):
    __tablename__ = "user_challenge_association"

    user_id = Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    challenge_id = Column(db.Integer, db.ForeignKey("challenges.id"), nullable=False)
    commited_to_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    done_at = Column(db.DateTime, nullable=True)
    succeeded = Column(db.Boolean, nullable=False, default=False)
    challenges = relationship("Challenge", backref="user_challenges")
    users = relationship("User", backref="user_challenges")

    def __init__(self, user_id, challenge_id, **kwargs):
        super().__init__(user_id=user_id, challenge_id=challenge_id, **kwargs)


class Category(PkModel):
    """A role for a challenge."""

    __tablename__ = "category"
    name = Column(db.String(80), unique=True, nullable=False)
    parent_id = Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    challenges = relationship("Challenge", backref="category")

    def __init__(self, name, parent_id, **kwargs):
        """Create instance."""
        super().__init__(name=name, parent_id=parent_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Category({self.name})>"


class Challenge(PkModel):
    """A challenge of the app."""

    __tablename__ = "challenges"
    challengename = Column(db.String(80), unique=True, nullable=False)
    description = Column(db.String(3000), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=False)
    category_id = Column(db.Integer, db.ForeignKey("category.id"))
    company_id = Column(db.Integer, db.ForeignKey("company.id"))
    co2offset = Column(db.Integer, nullable=False)
    chat_room_id = Column(db.String, db.ForeignKey("chat_rooms.room_id"))

    def __init__(
        self, challengename, description, active, category_id, co2offset, **kwargs
    ):
        """Create instance."""
        super().__init__(
            challengename=challengename,
            description=description,
            active=active,
            category_id=category_id,
            co2offset=co2offset,
            **kwargs,
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Challenge({self.challengename!r})>"
