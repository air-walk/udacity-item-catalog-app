from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session   = DBSession()


@app.route('/')
def helloWorld():
  return "Hello world!"


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 8000)
