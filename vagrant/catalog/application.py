from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session   = DBSession()


@app.route('/')
@app.route('/categories')
def showCategories():
  """Base route. Shows all categories and latest items."""
  categories = session.query(Category).all()
  return render_template('categories.html', categories = categories)


@app.route('/catalog/new/', methods=['GET', 'POST'])
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
  """Creates a new category."""
  if request.method == 'POST':
    newCategory = Category(name = request.form['name'])
    session.add(newCategory)
    session.commit()

    return redirect(url_for('showCategories'))
  else:
    return render_template('newCategory.html')


@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
  """Edits a category."""
  category = session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    category.name = request.form['name']
    session.commit()

    return redirect(url_for('showCategories'))
  else:
    return render_template('editCategory.html', category = category)


@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
  """Deletes a category."""
  category = session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    session.delete(category)
    session.commit()

    return redirect(url_for('showCategories'))
  else:
    return render_template('deleteCategory.html', category = category)


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
