from app import app, db
from app.forms import ItemForm, StoreForm
from flask import render_template, flash, redirect, request
from geopy.geocoders import Nominatim
from app.models import Stores, Items


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
        store = Stores.query.filter_by(longitude=longitude, latitude=latitude)

        if not store:
            flash("This store hasn't existed in the database.")
        else:
            new_item = Items(name=form.store_name.data,
                             description=form.item_description.data,
                             barcode=form.barcode.data)
            db.session.add(new_item)
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
            print(len(store))
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
