from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Item

app = Flask(__name__)


engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
	categories = session.query(Category).group_by(Category.name).all()
	items = session.query(Item).order_by(Item.created.desc()).all()
	return render_template('catalog.html', categories=categories, items=items)


@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
	#Need to check if an item with the same name already exists
	if request.method == 'POST':
		newItem = Item(name=request.form['name'], description=request.form['description'], category_id=request.form['category_id'])
		session.add(newItem)
		session.commit()
		return render_template('catalog.html')
	else:
		return render_template('additem.html')


@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
	#Optional: if list of items is empty, return custom message
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category = category).all()
	return render_template('catalog.html', categories=categories, category=category, items=items)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
	item = session.query(Item).filter_by(name=item_name).one()
	return render_template('item.html', item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
	return render_template('edititem.html', item=item)


@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
	return render_template('deleteitem.html', item=item)


if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)