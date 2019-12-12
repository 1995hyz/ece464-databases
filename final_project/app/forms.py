from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    store_name = StringField("Store Name", validators=[DataRequired()])
    item_name = StringField("Item Name", validators=[DataRequired()])
    item_dollar = IntegerField("Dollar", validators=[DataRequired()])
    item_cent = IntegerField("Cent", validators=[DataRequired()])
    item_description = StringField("Item Description")
    barcode = StringField("Barcode")
    submit = SubmitField("Submit")


class StoreForm(FlaskForm):
    store_name = StringField("Store Name", validators=[DataRequired()])
    street_addr = StringField()
