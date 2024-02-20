from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Float, DateTime
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    state = Column(String(20), default='START')
    avg_score = Column(Float)

    time_info = relationship("TimeInfo", back_populates="user", foreign_keys="TimeInfo.user_id", cascade="all, delete")

    def __repr__(self):
        return f"<User({self.id} {self.name})>"


class TimeInfo(Base):
    __tablename__ = 'time_info'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    retire_time = Column(DateTime(timezone=True), default=func.now())
    wakeup_time = Column(DateTime(timezone=True), default=func.now())
    sleep_duration = Column(Integer)
    sleep_score = Column(Float)

    user = relationship("User", back_populates="time_info", uselist=False)

    def __repr__(self):
        return f"<TimeInfo({self.id} {self.user_id} {self.sleep_score})>"
