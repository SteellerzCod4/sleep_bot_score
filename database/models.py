from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from bot_configs.states import States

from . import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    current_settings_id = Column(Integer, ForeignKey("time_settings.id", ondelete="CASCADE"))
    name = Column(String(30))
    age = Column(Integer)
    state = Column(Enum(States), default=States.START.value)
    avg_score = Column(Float)

    time_info = relationship("TimeInfo", back_populates="user", foreign_keys="TimeInfo.user_id", cascade="all, delete")
    time_settings = relationship("TimeSettings", back_populates="user", foreign_keys="TimeSettings.user_id",
                                 cascade="all, delete")

    def __repr__(self):
        return f"<User({self.id} {self.name} {self.age})>"


class TimeInfo(Base):
    __tablename__ = 'time_info'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    settings_id = Column(Integer, ForeignKey("time_settings.id", ondelete="CASCADE"), nullable=False)

    current_retire_time = Column(String)
    current_wakeup_time = Column(String)

    sleep_score = Column(Float)

    user = relationship("User", back_populates="time_info", uselist=False)
    time_settings = relationship("TimeSettings", back_populates="time_info", uselist=False)

    def __repr__(self):
        return f"<TimeInfo({self.id} {self.user_id} {self.sleep_score})>"


class TimeSettings(Base):
    __tablename__ = 'time_settings'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    best_retire_time = Column(String) #Column(DateTime(timezone=True), default=func.now())
    worst_retire_time = Column(String)

    best_wakeup_time = Column(String)
    worst_wakeup_time = Column(String)

    best_sleep_duration = Column(Float)

    user = relationship("User", back_populates="time_settings", foreign_keys=[user_id], uselist=False)
    time_info = relationship("TimeInfo", back_populates="time_settings", foreign_keys="TimeInfo.settings_id",
                             cascade="all, delete")

    def __repr__(self):
        return f"<TimeSettings({self.id} {self.user_id})>"
