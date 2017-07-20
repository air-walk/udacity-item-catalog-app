from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session   = DBSession()


@app.route('/')
def showCategories():
  """Base route. Shows all categories and latest items."""
  categories = session.query(Category).all()
  return render_template('categories.html', categories = categories)


@app.route('/catalog/<int:catalog_id>/items')
def showItems(catalog_id):
  """Shows all items for a catalog entry."""
  return "All items for a catalog entry..."


@app.route('/catalog/<int:catalog_id>/<int:item_id>')
def showItem(catalog_id, item_id):
  """Shows a particular item from a catalog entry."""
  return "A particular item for a catalog entry..."


@app.route('/catalog/<int:catalog_id>/<int:item_id>/edit')
def editItem(catalog_id, item_id):
  """Edits a particular item from a catalog entry."""
  return "Edit a particular item for a catalog entry..."


@app.route('/catalog/<int:catalog_id>/<int:item_id>/delete')
def deleteItem(catalog_id, item_id):
  """Deletes a particular item from a catalog entry."""
  return "Delete a particular item for a catalog entry..."


@app.route('/catalog.json')
def showCatalogJSON():
  """Shows catalog in JSON format"""
  return "Show catalog in JSON format..."


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 8000)
