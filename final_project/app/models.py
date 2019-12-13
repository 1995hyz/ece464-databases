from app import db


class Items(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(64))
    barcode = db.Column(db.String(32))
    prices = db.relationship("Prices", backref="items", lazy=True)
    inventory = db.relationship("Inventory", backref="items", lazy=True)

    def __repr__(self):
        return '<Items {}>'.format(self.username)


class Stores(db.Model):
    store_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    street = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), index=True, nullable=False)
    state = db.Column(db.String(8), nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    prices = db.relationship("Prices", backref="stores", lazy=True)
    inventory = db.relationship("Inventory", backref="stores", lazy=True)


class Prices(db.Model):
    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)


class Inventory(db.Model):
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), primary_key=True, nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), primary_key=True, nullable=True)
