from ...app import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, LargeBinary


class Photo(db.Model):
    __tablename__ = "photos"
    __bind_key__ = "photos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(100), nullable=True)
    
    
    def __repr__(self):
        return f"<Photo id={self.id} subtitle='{self.subtitle}'>"
