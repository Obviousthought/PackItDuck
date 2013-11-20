from wtforms import Form, TextField, TextAreaField, PasswordField, validators, DateField

class LoginForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    username = TextField("Username", [validators.Required()])  #    , validators.Username()])
    password = PasswordField("Password", [validators.Required()])

# class NewPostForm(Form):
#     title = TextField("title", [validators.Required()])
#     body = TextAreaField("body", [validators.Required()])

class NewTripForm(Form):
    name = TextField("name", [validators.Required()])
    start_date = DateField("start_date", [validators.Required()])
    end_date = DateField("end_date", [validators.Required()])