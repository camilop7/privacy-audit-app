from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class PingLog(Base):
    __tablename__ = "ping_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    gps = Column(JSON, nullable=True)
    screen = Column(JSON, nullable=True)
    org = Column(String, nullable=True)
    hostname = Column(String, nullable=True)
    source = Column(String, default="ping")  # "ping" or "manual"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
