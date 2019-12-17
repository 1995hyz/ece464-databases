from app import app, db
from app.forms import ItemForm, StoreForm, SearchForm, UpdateItemForm
from flask import render_template, flash, redirect, request, session, json, url_for
from app.models import Stores, Items, Prices
import datetime
import math
from sqlalchemy import func, update


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
            item_check = Items.query.filter_by(barcode=form.barcode.data, store_id=store[0].store_id).all()
            if len(item_check) != 0:
                flash("This item has existed in the store. Redirect to the Item Update Page.")
                # item_store = Stores.query.filter_by(store_id=item_check[0].store_id).first()
                messages = json.dumps({"store_id": item_check[0].store_id, "item_id": item_check[0].item_id})
                return redirect(url_for('.item_update', messages=messages))
            else:
                new_item = Items(name=form.item_name.data,
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


def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@app.route('/itemSearch', methods=['GET', 'POST'])
def item_searching():
    form = SearchForm()
    curr_lng = form.store_lng.data
    curr_lat = form.store_lat.data
    store_list = []
    header = ["Price", "Store Name", "Address", "Record Time"]
    if form.validate_on_submit():
        if form.barcode.data:
            search_result = Items.query.filter_by(barcode=form.barcode.data).all()
            if len(search_result) == 0:
                flash("The item is not in the database.")
                return redirect("/itemSearch")
            else:
                for result in search_result:
                    store = Stores.query.filter_by(store_id=result.store_id).first()
                    if haversine((float(curr_lat), float(curr_lng)), (float(store.latitude), float(store.longitude))) < 1000:
                        price = Prices.query.filter_by(store_id=store.store_id, item_id=result.item_id).\
                            group_by(Prices.price_id).having(func.max(Prices.time)).first()
                        store_list.append([str(price.price), store.name,
                                           ' '.join([store.street, store.city, store.state]), str(price.time)])
                return render_template("itemSearch.html", form=form, search_result=store_list, header=header)
        elif form.item_name.data:
            search_result = Items.query.filter(Items.name.ilike("%" + form.item_name.data + "%")).all()
            if len(search_result) == 0:
                flash("The item is not in the database.")
                return redirect("/itemSearch")
            else:
                for result in search_result:
                    store = Stores.query.filter_by(store_id=result.store_id).first()
                    if haversine((float(curr_lat), float(curr_lng)), (float(store.latitude), float(store.longitude))) < 1000:
                        price = Prices.query.filter_by(store_id=store.store_id, item_id=result.item_id).\
                            group_by(Prices.price_id).having(func.max(Prices.time)).first()
                        store_list.append([str(price.price), store.name,
                                           ' '.join([store.street, store.city, store.state]), str(price.time)])
                return render_template("itemSearch.html", form=form, search_result=store_list, header=header)
        else:
            flash("Please fill either the barcode or the item name field.")
            return redirect("/itemSearch")
    return render_template("itemSearch.html", form=form, search_result=[], header=header)


@app.route('/itemUpdate', methods=['GET', 'POST'])
def item_update():
    form = UpdateItemForm()
    messages = request.args['messages']
    messages = json.loads(messages)
    store = Stores.query.filter_by(store_id=messages["store_id"]).first()
    item = Items.query.filter_by(item_id=messages["item_id"]).first()
    if form.validate_on_submit():
        stmt = update(Items).where(Items.item_id == messages["item_id"]).values(description=form.item_description.data)
        new_price = Prices(time=datetime.datetime.now(),
                           price=float(str(form.item_dollar.data) + "." + str(form.item_cent.data)),
                           item_id=messages["item_id"],
                           store_id=messages["store_id"])
        db.session.add(new_price)
        db.session.commit()
        store = Stores.query.filter_by(store_id=messages["store_id"]).first()
        item = Items.query.filter_by(item_id=messages["item_id"]).first()
        return render_template("itemUpdate.html", form=form, store=store, item=item)
    return render_template("itemUpdate.html", form=form, store=store, item=item)
