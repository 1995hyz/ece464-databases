from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app.models import Items
from geopy.geocoders import Nominatim


class ItemForm(FlaskForm):
    store_name = StringField("Store Name", validators=[DataRequired()])
    item_name = StringField("Item Name", validators=[DataRequired()])
    item_dollar = IntegerField("Dollar", validators=[DataRequired()])
    item_cent = IntegerField("Cent", validators=[DataRequired()])
    item_description = StringField("Item Description")
    barcode = StringField("Barcode")
    submit = SubmitField("Submit")

    def validate_item(self, item_name):
        item = Items.query.filter_by(item_name=item_name.data, ).first()
        pass


class StoreForm(FlaskForm):
    store_name = StringField("Store Name", validators=[DataRequired()])
    street_addr = StringField("Street Addr", validators=[DataRequired()])
    city_name = StringField("City", validators=[DataRequired()])
    state_name = StringField("State", validators=[DataRequired()])
    submit = SubmitField("Submit")

    @staticmethod
    def validate_address():
        geolocator = Nominatim(user_agent="Store_Tracker")
        location = geolocator.geocode( )
