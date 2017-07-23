from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item
import json
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session   = DBSession()


@app.route('/login')
def login():
  """Shows login page to a user to sign in via Google sign in."""
  if user_is_logged_in():
    flash("You're currently logged in as %s. Please logout first if you'd like to login as a different user." %(get_user_name_from_login_session()))
    return redirect("/")

  return render_template('login.html')


@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
  """Responsible for getting authorization from user, and then accessing their Google data using Google APIs.
  This is also the auth endpoint which handles response from the OAuth2.0 server."""
  # Create the 'Flow' object based on client's secrets and scope
  flow = flow_from_clientsecrets('client_secrets.json',
                                  scope='https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                                  redirect_uri='http://localhost:8000/gconnect')
  flow.params['access_type']            = 'offline'
  flow.params['include_granted_scopes'] = 'true'        # For incremental authZ

  if request.method == 'POST':
    # Get the authorization URL and redirect the user to it, so that they can grant (or deny) application's access to their Google data
    auth_uri = flow.step1_get_authorize_url()
    print "[STEP 1]: Sending user to Google to authenticate him/herself and provide consent to the application.."

    return redirect(auth_uri)
  else:
    print "[STEP 2]: Received authZ consent/decline from user.."
    code = request.args.get('code')
    credentials = flow.step2_exchange(code)

    # Create an HTTP object and apply credentials to it so that all requests using this instance are authorized
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Send a request to Google+ API to get user info
    print "[STEP 3]: Attempting to retrieve user info from Google+.."
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo?alt=json"
    response     = http.request(userinfo_url)

    # If request succeeded, store the user's info in session and redirect to home page else route the user back to login page
    if response[0].status == 200:
      user_info = json.loads(response[1])

      login_session["email"]   = user_info["email"]
      login_session["name"]    = user_info["name"]
      login_session["picture"] = user_info["picture"]
      print "User identified as %s, redirecting to home page..." %(login_session["email"])

      flash("You successfully logged-in. Welcome!")
      return redirect("/")
    else:
      print "[" + response[0].status + " ERROR]: Something went wrong!"

      flash("Sorry, we were unable to log you in. Please check your username/password and try again.")
      return redirect(url_for("login"))


@app.route('/logout', methods=['POST'])
def logout():
  """Logs the user out of the application."""
  if login_session.get('email'):
    login_session.pop('email', None)
    login_session.pop('name', None)
    login_session.pop('picture', None)

    flash("You successfully logged-out. Goodbye!")
  else:
    flash("You're not logged-in, hence, no need to log-out. Redirected you to home page.")

  return redirect("/")


@app.route('/')
@app.route('/categories')
def showCategories():
  """Base route. Shows all categories and latest items."""
  categories = db_session.query(Category).all()
  return render_template('categories.html', categories = categories, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/new/', methods=['GET', 'POST'])
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
  """Creates a new category."""
  if request.method == 'POST':
    newCategory = Category(name = request.form['name'])
    db_session.add(newCategory)
    db_session.commit()

    flash("Category creation successful!")
    return redirect(url_for('showCategories'))
  else:
    return render_template('newCategory.html', user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/edit/', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
  """Edits a category."""
  category = db_session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    category.name = request.form['name']
    db_session.commit()

    flash("Category edit successful!")
    return redirect(url_for('showCategories'))
  else:
    return render_template('editCategory.html', category = category, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/delete/', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
  """Deletes a category."""
  category = db_session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    db_session.delete(category)

    # Once a category is deleted, delete related items as well
    items = db_session.query(Item).filter_by(cat_id = category_id).all()
    for item in items:
      db_session.delete(item)

    db_session.commit()

    flash("Category (and related items) deletion successful!")
    return redirect(url_for('showCategories'))
  else:
    return render_template('deleteCategory.html', category = category, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/items')
@app.route('/catalog/<int:category_id>/')
@app.route('/categories/<int:category_id>/items')
@app.route('/categories/<int:category_id>/')
def showItems(category_id):
  """Shows all items for a catalog entry."""
  category = db_session.query(Category).filter_by(id = category_id).one()
  items    = db_session.query(Item).filter_by(cat_id = category_id).all()

  return render_template('items.html', category = category, items = items, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/<int:item_id>')
@app.route('/categories/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):
  """Shows a particular item from a catalog entry."""
  item = db_session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  return render_template('item.html', item = item, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/new', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
  """Creates an item in catalog."""
  category = db_session.query(Category).filter_by(id = category_id).one()

  if request.method == 'POST':
    newItem = Item(cat_id = category_id, title = request.form['title'], description = request.form['description'])
    db_session.add(newItem)
    db_session.commit()

    flash("Item creation successful!")
    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('newItem.html', category = category, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
  """Edits a particular item from a catalog entry."""
  category = db_session.query(Category).filter_by(id = category_id).one()
  item     = db_session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  if request.method == 'POST':
    item.title       = request.form['title']
    item.description = request.form['description']
    db_session.commit()

    flash("Item edit successful!")
    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('editItem.html', category = category, item = item, user_is_logged_in = user_is_logged_in())


@app.route('/catalog/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
  """Deletes a particular item from a catalog entry."""
  category = db_session.query(Category).filter_by(id = category_id).one()
  item     = db_session.query(Item).filter_by(id = item_id, cat_id = category_id).one()

  if request.method == 'POST':
    db_session.delete(item)
    db_session.commit()

    flash("Item deletion successful!")
    return redirect(url_for('showItems', category_id = category_id))
  else:
    return render_template('deleteItem.html', category = category, item = item, user_is_logged_in = user_is_logged_in())


@app.route('/catalog.json')
@app.route('/categories.json')
def showCatalogJSON():
  """Shows catalog in JSON format"""
  categories = db_session.query(Category).all()
  return jsonify(category = [category.serialize for category in categories])


@app.route('/catalog/<int:category_id>.json')
@app.route('/categories/<int:category_id>.json')
def showItemsJSON(category_id):
  """Shows items in JSON format"""
  items = db_session.query(Item).filter_by(cat_id = category_id)
  return jsonify(item = [item.serialize for item in items])


def user_is_logged_in():
  return True if login_session.get("email") else False


def get_user_name_from_login_session():
  return login_session.get("name")

if __name__ == '__main__':
  import uuid

  # The secret key should actually be a secret, rather than out here in the open
  app.secret_key = "movement lifestyle" # str(uuid.uuid4())
  app.debug      = True
  app.run(host = '0.0.0.0', port = 8000)
