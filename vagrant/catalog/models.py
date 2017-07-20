from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):
      """Return category data in a serializeable format"""
      return {
          'id':   self.id,
          'name': self.name
      }


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    title = Column(String(250), nullable=False)
    cat_id = Column(Integer, ForeignKey('category.id'))
    cat = relationship(Category)

    @property
    def serialize(self):
      """Return item data in a serializeable format"""
      return {
          'id':          self.id,
          'description': self.description,
          'title':       self.title,
          'cat_id':      self.cat_id
      }


engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)