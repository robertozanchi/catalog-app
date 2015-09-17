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
	categories = session.query(Category).all()
	category = session.query(Category).filter_by(name=category_name).one()
	items = session.query(Item).filter_by(category = category).all()
	if items == []:
		return render_template('catalog.html', categories=categories, category=category, items=items, empty=True)
	else:
		return render_template('catalog.html', categories=categories, category=category, items=items)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
	item = session.query(Item).filter_by(name=item_name).one()
	return render_template('item.html', category_name=category_name, item=item, item_name=item_name)


@app.route('/catalog/<string:category_name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	item = session.query(Item).filter_by(name=item_name).one()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		if request.form['category_id']:
			item.category_id = request.form['category_id']
		session.add(item)
		session.commit()
		return redirect(url_for('showItems', category_name = category_name))
	else:
		return render_template('edititem.html', category_name=category_name, item=item, item_name=item_name)


@app.route('/catalog/<string:category_name>/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
	item = session.query(Item).filter_by(name=item_name).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deleteitem.html', category_name = category_name, item=item, item_name = item_name)


if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)