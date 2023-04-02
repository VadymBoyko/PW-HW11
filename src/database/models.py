from datetime import datetime, date

from sqlalchemy import Column, Integer, String, DateTime, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    notes = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @hybrid_property
    def days_to_next_birthday(self):
        next_birthday = self.birthday.replace(year=datetime.today().year)
        if next_birthday < datetime.today():
            next_birthday = datetime(next_birthday.year + 1, next_birthday.month, next_birthday.day)
        count_days = (next_birthday - datetime.today()).days
        return count_days
