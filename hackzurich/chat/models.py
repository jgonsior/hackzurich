# -*- coding: utf-8 -*-
"""Chat models."""
import datetime as dt


from hackzurich.database import (
    Column,
    PkModel,
    db,
    relationship,
    reference_col
)

class ChatRoom(PkModel):
    """ChatRoom contains various ChatMessages."""

    __tablename__ = "chat_rooms"
    room_id = Column(db.String(80), unique=True, nullable=False)
    name = Column(db.String(80), unique=False, nullable=True)

    def __init__(self, room_id, **kwargs):
        """Create instance."""
        super().__init__(room_id=room_id, name=room_id **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ChatRoom({self.room_id})>"


class ChatMessage(PkModel):
    """A ChatMessage ."""

    __tablename__ = "chat_messages"
    text = Column(db.String(180), unique=False, nullable=False)
    written_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    chat_room_id = reference_col("chat_rooms", nullable=True)
    room = relationship("ChatRoom", backref="chat_messages")

    user_id = reference_col('users', nullable=True)
    user = relationship("User", backref="chat_messages")

    def __init__(self, text, **kwargs):
        """Create instance."""
        super().__init__(
            text=text
            **kwargs,
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ChatMessage({self.text!r})>"
