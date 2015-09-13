from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
	return "This is the catalog home page"


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