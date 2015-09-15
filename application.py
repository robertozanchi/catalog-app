from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)


category = {'name': 'Basketball', 'id':'1'}
categories = [{'name': 'Basketball', 'id':'1'}, {'name': 'Baseball', 'id':'2'}, {'name': 'Snowboarding', 'id':'3'}]

item = {'name':'Goggles', 'id':'1', 'category_id':'1', 'description':'like glasses', 'category':'Snowboarding'}
items = [{'name':'Goggles', 'id':'1', 'category_id':'3'},{'name':'Bat', 'id':'2', 'category_id':'2'},
		 {'name':'Ball', 'id':'3', 'category_id':'1'} ]


@app.route('/')
@app.route('/catalog/')
def showCatalog():
	return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/add/')
def addItem():
	return render_template('additem.html')


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items/')
def showItems(category_id):
	return render_template('items.html', category_id=category_id, categories=categories, items=items)


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def showItem(category_id, item_id):
	return render_template('item.html', category_id=category_id, categories=categories, item=item, items=items)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
	return render_template('edititem.html', item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
	return "This page allows loggedin users to delete an item they created"


if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)