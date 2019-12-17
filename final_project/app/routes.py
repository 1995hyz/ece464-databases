from app import app, db
from app.forms import ItemForm, StoreForm, SearchForm
from flask import render_template, flash, redirect, request
from app.models import Stores, Items, Prices
import datetime


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/itemRegistration', methods=['GET', 'POST'])
def item_registration():
    form = ItemForm()

    if form.validate_on_submit():
        longitude = form.store_lng.data
        latitude = form.store_lat.data
        store = Stores.query.filter_by(longitude=longitude, latitude=latitude).all()
        if len(store) == 0:
            flash("This store hasn't existed in the database.")
        else:
            item_check = Items.query.filter_by(barcode=form.barcode.data).all()
            if len(item_check) != 0:
                flash("This item has existed in the store. Redirecting to the Item Update Page...")
                return redirect("/itemUpdate.html")
            else:
                new_item = Items(name=form.store_name.data,
                                 description=form.item_description.data,
                                 barcode=form.barcode.data,
                                 store_id=store[0].store_id)
                db.session.add(new_item)
                db.session.commit()
                new_item = Items.query.filter_by(barcode=form.barcode.data).all()
                new_price = Prices(time=datetime.datetime.now(),
                                   price=float(str(form.item_dollar.data) + "." + str(form.item_cent.data)),
                                   item_id=new_item[0].item_id,
                                   store_id=store[0].store_id)
                db.session.add(new_price)
                db.session.commit()
                flash("New item has been successfully added.")
                return redirect("/itemRegistration")
    return render_template("itemRegistration.html", title="Item Registration", form=form)


@app.route('/storeRegistration', methods=['GET', 'POST'])
def store_registration():
    form = StoreForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            longitude = form.store_lng.data
            latitude = form.store_lat.data
            store = Stores.query.filter_by(longitude=longitude, latitude=latitude).all()
            if len(store) != 0:
                flash("This store has existed in the database.")
            else:
                new_store = Stores(name=form.store_name.data,
                                   street=form.street_addr.data,
                                   city=form.city_name.data,
                                   state=form.state_name.data,
                                   longitude=longitude,
                                   latitude=latitude)
                db.session.add(new_store)
                db.session.commit()
                flash("New store has been successfully added.")
            return redirect("/storeRegistration")

    return render_template("storeRegistration.html", title="Store Registration", form=form)


@app.route('/itemSearch', methods=['GET', 'POST'])
def item_searching():
    form = SearchForm()
    if form.validate_on_submit():
        if form.barcode.data:
            search_result = Items.query.filter_by(barcode=form.barcode.data).all()
            if search_result is None:
                flash("The item is not in the database.")
                return redirect("/itemSearch")
            else:
                pass
