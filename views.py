from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Trip, PackingList, PackListItems, Item, ActivityItem, Activity, TripActivity
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
import config
import forms
import model
import datetime

app = Flask(__name__)
app.config.from_object(config)

def format_datetime(date, fmt='%c'):
    # check whether the value is a datetime object
    if not isinstance(date, (datetime.date, datetime.datetime)):
        try:
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception, e:
            return date
    return date.strftime(fmt)

app.jinja_env.filters['datetime'] = format_datetime

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

Markdown(app)

##### Routes

@app.route("/")
def index():
    if session.get('username'):
        username = session['username']
        user = model.get_user_by_username(username)
        return redirect(url_for("profile", username=username))
    else:
        return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def authenticate():

    form = forms.LoginForm(request.form)
    username = form.username.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")
    else:
        login_user(user)
        return redirect(url_for("profile", username=username))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_user():
    email=request.form.get("email")
    username=request.form.get("username")
    password=request.form.get("password")
    verify_password=request.form.get("password_verify")

    if model.email_exists(email):
        flash("Email already exists!")
        return redirect(url_for("register"))
    if model.username_exists(username):
        flash("Username is already taken!")
        return redirect(url_for("register"))
    if password != verify_password:
        flash("Passwords do not match!")
        return redirect(url_for("register"))

    model.create_user(email, username, password)
    user = model.get_user_by_username(username)

    return redirect(url_for("profile", username=username))

@app.route("/profile/<username>")
@login_required
def profile(username):
    # user = model.get_user_by_username(username)
    session_user_id = session.get('id')
    user_id = session['user_id']
    user = model.get_user_by_id(user_id)
    packlist_id = model.get_user_packlist(user_id)
    trip_names = model.get_user_trip_names(user_id)
    # packlist_items = model.get_


    return render_template("home_page.html", user_id=user_id, username=user.username, packlist_id=packlist_id, trip_names=trip_names, email=user.email)


@app.route("/new_trip")
@login_required
def new_trip():
    return render_template("new_trip.html")

@app.route("/new_trip", methods=["POST"])
@login_required
def create_trip():
    form = forms.NewTripForm(request.form)
    if not form.validate():
        flash("All fields must be filled!")
        return render_template("new_trip.html")
    name = request.form.get("name")
#    destination = request.form.get("destination")
    start_date= request.form.get("start_date")
    end_date=request.form.get("end_date")
    # Create the Trip
    model.create_trip(name) # add DESTINATION, start_date, end_date

#### THIS IS NOT WORKING! FIX IT!!!!

    # session_trip_name = session.get('name')
    name = session['session_trip_name']
    trip = model.get_trip_by_name(name)
    user = get_user_by_trip_id(trip.id)
    # Create the Packing List
    model.create_packinglist(trip_id=trip.id, user_id=user.id)

    return redirect(url_for("packing_list", trip_id=trip.id, user_id=user.id))

@app.route("/<trip_name>")
@login_required
def packing_list(trip_id):
    trip = model.get_trip_by_id(trip_id)
    list_of_items = model.session.query(Item).filter_by(name).all()

    return render_template("packing_list.html", trip=trip, list_of_items=list_of_items)   


@app.route("/logout")
# @login_required
def logout():
    session.clear()
    # logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    admin = Admin(app)
    admin.add_view(ModelView(model.User, model.session))
    admin.add_view(ModelView(model.Trip, model.session))
    admin.add_view(ModelView(model.PackingList, model.session))
    admin.add_view(ModelView(model.PackListItems, model.session))
    admin.add_view(ModelView(model.Activity, model.session))
    admin.add_view(ModelView(model.Item, model.session))
    admin.add_view(ModelView(model.TripActivity, model.session))
    admin.add_view(ModelView(model.ActivityItem, model.session))
    app.run(debug = True)













