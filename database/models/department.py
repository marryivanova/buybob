from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    employees = relationship("Employee", back_populates="department")
