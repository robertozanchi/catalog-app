from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


category = {'name': 'Basketball', 'id':'1'}
categories = [{'name': 'Basketball', 'id':'1'}, {'name': 'Baseball', 'id':'2'}, {'name': 'Snowboarding', 'id':'3'}]

item = {'name':'Goggles', 'id':'1', 'category_id':'1'}
items = [{'name':'Goggles', 'id':'1', 'category_id':'3'},{'name':'Bat', 'id':'2', 'category_id':'2'},
		 {'name':'Ball', 'id':'3', 'category_id':'1'} ]


@app.route('/')
@app.route('/catalog/')
def showCatalog():
	return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/add/')
def addItem():
	return "Logged in users can add an item from the home page"


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
	return "This page shows all items in a category"


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
	return "This page shows detail for a selected items"


@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
	return "This page allows loggedin users to edit an item they created"


@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
	return "This page allows loggedin users to delete an item they created"


if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)