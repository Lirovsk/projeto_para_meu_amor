from ...app import db

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class Music(db.Model):
    __tablename__ = "musics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    
    
    def __repr__(self):
        return f"<Music id={self.id} url='{self.url}'>"



class SeenMusic(db.Model):
    __tablename__ = "musics"
    __bind_key__ = "seen"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    
    
    def __repr__(self):
        return f"<SeenMusic id={self.id} music_id={self.url}>"
