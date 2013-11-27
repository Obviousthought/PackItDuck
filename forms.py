from wtforms import Form, SelectField, TextField, TextAreaField, PasswordField, validators, DateField, DateTimeField
# , RadioField, widgets, SelectMultipleField

class LoginForm(Form):
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])

class RegisterForm(Form):
    email = TextField("email", [validators.Required()])
    username = TextField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])
    password_verify = PasswordField("password_verify", [validators.Required()])

class NewTripForm(Form):
    name = TextField("trip_name", [validators.Required()])
    # destination = TextField("destination", [validators.Required()])
    start_date = DateField("start_date")
    	# , [validators.Required()])
    end_date = DateField("end_date")
    	# , [validators.Required()])
    activity = SelectField("activity")
    # activity_list = SelectMultipleField("activity_list", choices=[], coerce=unicode, option_widget=None)