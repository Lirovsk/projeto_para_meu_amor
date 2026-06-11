from ...app import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Message(db.Model):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<Message id={self.id} content='{self.content}'>"


class SeenMessage(db.Model):
    __tablename__ = "messages"
    __bind_key__ = "seen"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    
    def __repr__(self):
        return f"<SeenMessage id={self.id} message_id={self.content}>"
