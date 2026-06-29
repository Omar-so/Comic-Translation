from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# models/chapter.py
from .base import Base

class Chapter(Base):
    __tablename__ = "chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    comic_name: Mapped[str] = mapped_column(String(50))
    canvas_url_before: Mapped[str] = mapped_column(String(50))
    canvas_url_after: Mapped[str] = mapped_column(String(50) )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
    user: Mapped["User"] = relationship(back_populates="chapters")
