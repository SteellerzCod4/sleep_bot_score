from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Float
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(String(9), nullable=False, unique=True, primary_key=True)
    state = Column(String(20), default='START')
    avg_score = Column(Float)

    def __repr__(self):
        return f"<User({self.id} {self.name})>"
