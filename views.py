from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User, Trip, PackingList, PackListItems, Item, ActivityItem, Activity, TripActivity
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flaskext.markdown import Markdown
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
import config
import forms
import model
import datetime
# from flask_peewee.auth import Auth
# from flask_peewee.db import Database
# from config import db

app = Flask(__name__)
app.config.from_object(config)


# auth = Auth(app, db, user_model=User)

# def format_datetime(date, fmt='%c'):
#     # check whether the value is a datetime object
#     if not isinstance(date, (datetime.date, datetime.datetime)):
#         try:
#             date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
#         except Exception, e:
#             return date
#     return date.strftime(fmt)

# app.jinja_env.filters['datetime'] = format_datetime

login_manager = LoginManager()
# login_manager.setup_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return model.session.query(User).get(user_id)
    # User.query.get(int(id))

Markdown(app)

##### Routes

@app.route("/")
def index():
    # if auth.get_logged_in_user():
    #     username = current_user.username
    #     return redirect(url_for("profile", username=username))
    # else:
    #     return render_template("index.html")

    if session.get('username'):
        username = session['username']
        user = model.get_user_by_username(username)
        return redirect(url_for("profile", username=username))
    else:
        return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def authenticate():
    if current_user.is_authenticated():
        return redirect(url_for('profile', username=current_user.username))

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
    # user = auth.get_logged_in_user()
    # print current_user
    user_id = current_user.id
    packlist_id = model.get_user_packlist(user_id)
    trip_names = model.get_user_trip_names(user_id)
    #####   Write code that will return a single packing_list id when queried within the html page (aka when the user clicks on the link with the trip name that will redirect them to the packinglist page, but via packing_list_id)

    # packing_list = model.session.query(PackingList).filter_by(trip_id=trip.id).one()

    ####
    # user_trips = model.session.query(Trip).filter_by(user_id=user_id).all()
    # for trip in user_trips:


    ## Consider making either tuples of trip names and packing_list_id's or figuring out how to call within html for a dictionary (key=trip name, value=packing_list_id)

    return render_template("home_page.html", user_id=user_id, username=current_user.username, packlist_id=packlist_id, trip_names=trip_names)


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
    # start_date= request.form.get("start_date")
    # end_date=request.form.get("end_date")
    # Create the Trip
    user_id = current_user.id
    model.create_trip(user_id=user_id, name=name) # add DESTINATION, start_date, end_date
    trip = model.get_trip_by_name(name=name)
    # Create the Packing List
    model.create_packinglist(user_id=trip.user_id, trip_id=trip.id)
    packing_list = model.session.query(PackingList).filter_by(trip_id=trip.id).one()

    return redirect(url_for("packing_list", packlist_id=packing_list.id))
#### ABOVE IS NOT WORKING! FIX IT!!!!


@app.route("/<trip_name>")
@login_required
def packing_list(packlist_id):
    trip = model.get_trip_by_packlist_id(packlist_id)
    list_of_items = model.get_list_of_items()
    user_trips = model.get_user_trip_names(trip.user_id)

    return render_template("packing_list.html", user_trips=user_trips, list_of_items=list_of_items, trip=trip)   


@app.route("/logout")
def logout():
    # session.clear()
    logout_user()
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













