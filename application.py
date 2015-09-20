from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Udacity Catalog Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# Connect: sign a user into Google+ 
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.to_json()
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 100px; height: 100px;border-radius:\
               50px;-webkit-border-radius: 50px;-moz-border-radius: 50px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect: revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html', response='Currently not connected.')
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html', response='Successfully disconnected.')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html', response='Error: Failed to revoke token.')


# Catalog web app home page
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category).group_by(Category.name).all()
    items = session.query(Item).order_by(Item.created.desc()).all()
    return render_template('catalog.html', categories=categories, items=items,
                           login_session=login_session)


# Add new item to the catalog
@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    categories = session.query(Category).group_by(Category.name).all()
    items = session.query(Item).order_by(Item.created.desc()).all()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(name=request.form['name'],
                       description=request.form['description'],
                       category_id=request.form['category_id'],
                       image=request.form['image'], user_id=request.form['user_id'])
        # Check if an item with the same name already exist
        for i in items:
            if newItem.name in i.name:
                flash("Error: an item with name "+newItem.name+" already exists.\
                      Enter a different item.")
                return render_template('catalog.html', categories=categories, items=items,
                                       login_session=login_session)
        session.add(newItem)
        session.commit()
        flash("New item created")
        return render_template('catalog.html', categories=categories, items=items,
                               login_session=login_session)
    else:
        logged_user = session.query(User).filter_by(email=login_session['email']).one()
        return render_template('additem.html', categories=categories,
                               logged_user=logged_user, login_session=login_session)


# List items by category on the home page
@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category = category).all()
    if items == []:
        return render_template('catalog.html', categories=categories,
                               category=category, items=items, empty=True,
                               login_session=login_session)
    else:
        return render_template('catalog.html', categories=categories, 
                               category=category, items=items,
                               login_session=login_session)


# Individual item page
@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    return render_template('item.html', category_name=category_name, 
                           item=item, item_name=item_name,
                           login_session=login_session )


# Edit an item - requires login and only owner can edit
@app.route('/catalog/<string:category_name>/<string:item_name>/edit/',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    categories = session.query(Category).group_by(Category.name).all()
    item = session.query(Item).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized\
               to edit this item.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category_id']:
            item.category_id = request.form['category_id']
        session.add(item)
        session.commit()
        flash("Item successfully edited")
        return redirect(url_for('showItems', category_name = category_name,
                                login_session=login_session))
    else:
        return render_template('edititem.html', categories=categories,
                               category_name=category_name, item=item,
                               item_name=item_name, login_session=login_session)


# Delete an item - requires login and only owner can delete
@app.route('/catalog/<string:category_name>/<string:item_name>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    item = session.query(Item).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to \
               delete this item.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item deleted")
        return redirect(url_for('showCatalog', login_session=login_session))
    else:
        return render_template('deleteitem.html', category_name = category_name,
                               item=item, item_name = item_name)


# JSON API endpoint for catalog home page
@app.route('/JSON')
@app.route('/catalog/JSON')
def showCatalogJSON():
    items = session.query(Item).order_by(Item.created.desc()).all()
    return jsonify(Items=[i.serialize for i in items])


# XML API endpoint for catalog home page
@app.route('/xml')
@app.route('/catalog/xml')
def showCatalogXML():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.created.desc()).all()
    template = render_template('catalog.xml', categories=categories, items=items)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response


if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)