from app import app
from app.forms import ItemForm, StoreForm
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/itemRegistration')
def item_registration():
    form = ItemForm()
    return render_template("itemRegistration.html", title="Item Registration", form=form)


@app.route('/storeRegistration')
def store_registration():
    form = StoreForm()