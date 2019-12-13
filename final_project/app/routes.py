from app import app, db
from app.forms import ItemForm, StoreForm
from flask import render_template, flash, redirect
from geopy.geocoders import Nominatim
from app.models import Stores


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/itemRegistration', methods=['GET', 'POST'])
def item_registration():
    form = ItemForm()
    if form.validate_on_submit():
        input_addr = form.street_addr.data + " " + form.city_name.data + " " + form.state_name.data
        geolocator = Nominatim(user_agent="store_searcher")
        location = geolocator.geocode(input_addr)
        if location is None:
            flash("Cannot find such address.")
        store = Stores.query.filter_by(longtitude=float(location.longitude), latitude=float(location.latitude))
        if store:
            flash("This store has existed in the database.")
        else:
            new_store = Stores(name=form.store_name.data,
                               street=form.street_addr.data,
                               city=form.city_name.data,
                               state=form.state_name.data,
                               longitude=location.longitude,
                               latitude=location.latitude)
            db.session.add(new_store)
            db.session.commit()
            flash("New store has been successfully added.")
            return redirect("/storeRegistration")

    return render_template("itemRegistration.html", title="Item Registration", form=form)


@app.route('/storeRegistration', methods=['GET', 'POST'])
def store_registration():
    form = StoreForm()
    return render_template("storeRegistration.html", title="Store Registration", form=form)
