from sqlalchemy import Column, String
from appv1.models.base_class import Base

class Module(Base):
    __tablename__ = 'modules'
    module_name = Column(String(15), primary_key=True)
