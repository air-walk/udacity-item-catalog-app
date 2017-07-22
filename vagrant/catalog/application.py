from flask import Flask, render_template, request, redirect, url_for, jsonify
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


@app.route('/catalog/<int:category_id>/items')
@app.route('/catalog/<int:category_id>/')
@app.route('/categories/<int:category_id>/items')
@app.route('/categories/<int:category_id>/')
def showItems(category_id):
  """Shows all items for a catalog entry."""
  category = session.query(Category).filter_by(id = category_id).one()
  items    = session.query(Item).filter_by(cat_id = category_id)

  return render_template('items.html', category = category, items = items)


@app.route('/catalog/<int:category_id>/<int:item_id>')
@app.route('/categories/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
  """Shows a particular item from a catalog entry."""
  item = session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  return render_template('item.html', item = item)


@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
  """Creates an item in catalog."""
  category = session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    newItem = Item(cat_id = category_id, title = request.form['title'], description = request.form['description'])
    session.add(newItem)
    session.commit()

    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('newItem.html', category = category)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
  """Edits a particular item from a catalog entry."""
  category = session.query(Category).filter_by(id = category_id).one()
  item     = session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  if request.method == 'POST':
    item.title       = request.form['title']
    item.description = request.form['description']
    session.commit()

    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('editItem.html', category = category, item = item)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
  """Deletes a particular item from a catalog entry."""
  category = session.query(Category).filter_by(id = category_id).one()
  item     = session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  if request.method == 'POST':
    session.delete(item)
    session.commit()

    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('deleteItem.html', category = category, item = item)


@app.route('/catalog.json')
@app.route('/categories.json')
def showCatalogJSON():
  """Shows catalog in JSON format"""
  categories = session.query(Item).all()
  # for category in categories:
  #  category.

  return jsonify(category = [category.serialize for category in categories])


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 8000)
