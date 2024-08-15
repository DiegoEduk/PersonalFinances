from datetime import datetime
from sqlalchemy import CHAR, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, String
from appv1.models.base_class import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    user_id = Column(CHAR(30), primary_key=True)
    full_name = Column(String(80))
    mail = Column(String(100), unique=True)
    passhash = Column(String(140))
    user_role = Column(String(15), ForeignKey('roles.rol_name'))
    user_status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

role = relationship("Role")
