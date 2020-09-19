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


#  class Category_Challenges(


class Category(PkModel):
    """A role for a challenge."""

    __tablename__ = "category"
    name = Column(db.String(80), unique=True, nullable=False)
    parent_id = Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

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
    category_id = Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __init__(self, challengename, description, active, category_id, **kwargs):
        """Create instance."""
        super().__init__(
            challengename=challengename,
            description=description,
            active=active,
            category_id=category_id,
            **kwargs,
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Challenge({self.challengename!r})>"
