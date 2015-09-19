
import os
import sys
import datetime
# include sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

"""User class"""
class User(Base):
    __tablename__ = 'Users'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    picture = Column(String(255))

"""Category class"""
class Category(Base):
    __tablename__ = 'Categories'

    name = Column(String(255), nullable = False)
    id = Column(Integer, primary_key = True)

"""Item class"""
class Item(Base):
    __tablename__ = 'Items'

    name = Column(String(255), nullable = False)
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer,ForeignKey('Categories.id'))
    category = relationship(Category)
    user_id = Column(Integer,ForeignKey('Users.id'))
    user = relationship(User)
    description = Column(String(255))
    image = Column(String(255))
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        return {
                'name': self.name,
                'category': self.category.name,
                'description': self.description
        }
    

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)