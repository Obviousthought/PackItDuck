from wtforms import Form, SelectField, SelectMultipleField, TextField, TextAreaField, PasswordField, validators, DateField, DateTimeField
from wtforms.validators import Required, optional
# , QuerySelectField, QueryMultipleSelectField, ModelSelectField, widgets
# from wtforms.fields import Field
# from wtforms.validators import ValidationError
# from model import User, Trip, PackingList, PackListItems, Item, ActivityItem, Activity, TripActivity
# from operator import attrgetter


class LoginForm(Form):
	username = TextField("username", validators=[validators.Required()])
	password = PasswordField("password", validators=[validators.Required()])

class RegisterForm(Form):
	email = TextField("email", validators=[validators.Required()])
	username = TextField("username", validators=[validators.Required()])
	password = PasswordField("password", validators=[validators.Required()])
	password_verify = PasswordField("password_verify", validators=[validators.Required()])


class NewTripForm(Form):
	name = TextField("trip_name", validators=[validators.Required()])
	destination = TextField("destination", validators=[validators.Required()])
	start_date = DateField("start_date", validators=[validators.optional()])
	end_date = DateField("end_date")
	activity = SelectField("activity", coerce=int, validators=[validators.optional()])



# , validators=[validators.Required()]
