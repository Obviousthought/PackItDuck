from wtforms import Form, SelectField, TextField, TextAreaField, PasswordField, validators, DateField, DateTimeField
# , RadioField, widgets, SelectMultipleField

class LoginForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    username = TextField("Username", [validators.Required()])  #    , validators.Username()])
    password = PasswordField("Password", [validators.Required()])

# class NewPostForm(Form):
#     title = TextField("title", [validators.Required()])
#     body = TextAreaField("body", [validators.Required()])

class NewTripForm(Form):
    name = TextField("name", [validators.Required()])
    # destination = TextField("destination", [validators.Required()])
    start_date = DateField("start_date")
    	# , [validators.Required()])
    end_date = DateField("end_date")
    	# , [validators.Required()])
    # activity = RadioField("activity")
    activity = SelectField("activity")
    # activity_list = SelectMultipleField("activity_list", choices=[], coerce=unicode, option_widget=None)