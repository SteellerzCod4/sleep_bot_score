from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String(9), nullable=False, unique=True, primary_key=True)
    state = Column(String(20), default='START')
    name = Column(String(30))
    last_name = Column(String(30))
    gender = Column(String(1))
    link_photo = Column(String(50))
    description = Column(Text(200))
    location = Column(String(50))
    is_active = Column(Boolean)

    def __repr__(self):
        return f"<User({self.id} {self.name})>"
