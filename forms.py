from wtforms import Form, TextField, TextAreaField, PasswordField, validators

class LoginForm(Form):
    email = TextField("Email", [validators.Required(), validators.Email()])
    username = TextField("Username", [validators.Required()])  #    , validators.Username()])
    password = PasswordField("Password", [validators.Required()])

# class NewPostForm(Form):
#     title = TextField("title", [validators.Required()])
#     body = TextAreaField("body", [validators.Required()])
