# -*- coding: utf-8 -*-
"""Chat models."""
import datetime as dt

from sqlalchemy.ext.orderinglist import ordering_list

from flask_login import current_user

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
    challenges = relationship("Challenge", backref="chat_room")

    def __init__(self, room_id, **kwargs):
        """Create instance."""
        super().__init__(room_id=room_id, name=room_id **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ChatRoom({self.room_id})>"

    def get_history(self, num=20):
        """History is a json representation of the last num chat messages in reverse order [{}, {}, ...]."""
        if len(self.chat_messages) > num:
            msg = self.chat_messages[-num:]
        else:
            msg = self.chat_messages
        return [m.get_json() for m in msg]


class ChatMessage(PkModel):
    """A ChatMessage ."""

    __tablename__ = "chat_messages"
    text = Column(db.String(180), unique=False, nullable=False)
    written_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    chat_room_id = reference_col("chat_rooms", nullable=True)
    room = relationship("ChatRoom", backref="chat_messages", collection_class=ordering_list('written_at'))

    user_id = reference_col('users', nullable=True)
    user = relationship("User", backref="chat_messages")

    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(
            **kwargs
        )

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<ChatMessage({self.text!r})>"

    def get_json(self):
        """A json representation of the chat message, who, when what."""
        # ISO 8601 datetime format
        d = {'text': self.text, 'written_at': self.written_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z')}
        if self.user:
            d['user'] = self.user.username
            d['is_self'] = self.user == current_user
        else:
            d['user'] = 'anonymous'
            d['is_self'] = False
        return d
