from sqlalchemy import Column, Integer
from database import Base

class WatchEventDB(Base):
    __tablename__ = "watch_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    video_id = Column(Integer, index=True)
    seconds_watched = Column(Integer)
