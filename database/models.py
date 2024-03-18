from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from bot_configs.states import States

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    name = Column(String(30))
    age = Column(Integer)
    state = Column(Enum(States), default=States.START.value)
    avg_score = Column(Float)

    time_info = relationship("TimeInfo", back_populates="user", foreign_keys="TimeInfo.user_id", cascade="all, delete")

    def __repr__(self):
        return f"<User({self.id} {self.name} {self.age})>"


class TimeInfo(Base):
    __tablename__ = 'time_info'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    current_retire_time = Column(DateTime(timezone=True), default=func.now())
    best_retire_time = Column(DateTime(timezone=True), default=func.now())
    worst_retire_time = Column(DateTime(timezone=True), default=func.now())

    current_wakeup_time = Column(DateTime(timezone=True), default=func.now())
    best_wakeup_time = Column(DateTime(timezone=True), default=func.now())
    worst_wakeup_time = Column(DateTime(timezone=True), default=func.now())

    best_sleep_duration = Column(Float)

    sleep_score = Column(Float)

    user = relationship("User", back_populates="time_info", uselist=False)

    def __repr__(self):
        return f"<TimeInfo({self.id} {self.user_id} {self.sleep_score})>"
