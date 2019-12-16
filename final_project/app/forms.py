from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from app.models import Items, Stores
from geopy.geocoders import Nominatim


class ItemForm(FlaskForm):
    store_lng = StringField("lng", validators=[DataRequired()])
    store_lat = StringField("lat", validators=[DataRequired()])
    store_name = StringField("Store Name", validators=[DataRequired()])
    item_name = StringField("Item Name", validators=[DataRequired()])
    item_dollar = IntegerField("Dollar", validators=[DataRequired()])
    item_cent = IntegerField("Cent", validators=[DataRequired()])
    item_description = StringField("Item Description")
    barcode = StringField("Barcode")
    submit = SubmitField("Submit")

    def validate_name(self, store_name):
        store = Stores.query.filter_by(item_name=store_name.data).first()
        if not store:
            raise ValidationError("The Store isn't existed in the database.")


class StoreForm(FlaskForm):
    store_lng = StringField("lng", validators=[DataRequired()])
    store_lat = StringField("lat", validators=[DataRequired()])
    store_name = StringField("Store Name", validators=[DataRequired()])
    street_addr = StringField("Street Addr", validators=[DataRequired()])
    city_name = StringField("City", validators=[DataRequired()])
    state_name = StringField("State", validators=[DataRequired()])
    submit = SubmitField("Submit")

    @staticmethod
    def validate_address():
        geolocator = Nominatim(user_agent="Store_Tracker")

