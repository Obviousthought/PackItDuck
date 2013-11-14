from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Trip, PackingList, PackListItems, Item, ActivityItem, Activity
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model

app = Flask(__name__)
app.config.from_object(config)

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    print User.query.get(user_id)
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

@app.route("/")
def index():
    if session.get('id'):
        user = model.user_by_id(session['id'])
    # user = load_user(user_id)
    # if user != None:
        return redirect(url_for("my_profile", user_id=user.id))
    else:
        return render_template("index.html", user_id=None)

@app.route("/", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("index.html")

    username = form.username.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("index.html")

    login_user(user)
    return redirect(request.args.get("next", url_for("my_profile")))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def make_new_user():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    verify_password = request.form.get("password_verify")
    
    if password != verify_password:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    if model.userExists(username, email):
        flash("Account already exists for username and/or email") 
        return redirect(url_for("register"))

    model.create_user(email, username, password)
    flash("You've successfully made an account!")
    user = User.query.filter_by(username=username).first()

#### Problem right here:
    login_user(user)
    return redirect(request.args.get("next", url_for("my_profile")))

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("index"))



@app.route("/profile/<user_id>")
@login_required
def my_profile(user_id):
    profile_link = user_profile_link()
    user = load_user(user_id)
    user_trips = model.get_user_trips(user_id)
    return render_template("home_page.html", user_id=user_id, username = user.username, user_trips=user_trips, profile_link=profile_link)

def user_profile_link():
    if session.get('id'):
        profile_link = session['id']
    else:
        profile_link = None
    return profile_link



if __name__ == "__main__":
    app.run(debug=True)
