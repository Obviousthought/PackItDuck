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
import pdb


app = Flask(__name__)
app.config.from_object(config)


login_manager = LoginManager()
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
    if current_user.is_authenticated():
        return redirect(url_for("profile", username=current_user.username))
    else:
        return render_template("login.html")


@app.route("/login")
def login():
    if current_user.is_authenticated():
        return redirect(url_for("profile", username=current_user.username))
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    username = form.username.data
    password = form.password.data

    user = model.session.query(User).filter_by(username=username).first()
    # user = model.get_user_by_username(username)

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")
    else:
        login_user(user)
        current_user = user
        return redirect(url_for('profile', username=user.username))

@app.route("/register")
def register():
    if current_user.is_authenticated():
        return redirect(url_for('profile', username=current_user.username))
    else:
        return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_user():
    form = forms.RegisterForm(request.form)
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
    login_user(user)
    return redirect(url_for("profile", username=username))

@app.route("/profile/<username>")
@login_required
def profile(username):
    user = current_user
    # user_id = current_user.id
    packlist_id = model.get_user_packlist(user.id)
    # trip_names = model.get_user_trip_names(user.id)
    trip_list = model.get_user_trips(user.id)

    return render_template("home_page.html", user_id=user.id, username=user.username, packlist_id=packlist_id, trip_list=trip_list)


@app.route("/new_trip")
@login_required
def new_trip():
    activities = model.session.query(Activity).all()
    return render_template("new_trip.html", activities=activities)

@app.route("/new_trip", methods=["POST"])
@login_required
def create_trip():
    user = current_user
    form = forms.NewTripForm(request.form)
    # form.activities.choice = [(g.id, g.name) for g in model.session.query(Activity).order_by('name')]
    trip_name = request.form.get("trip_name")
#    destination = request.form.get("destination")
    start_date= request.form.get("start_date")
    end_date= request.form.get("end_date")
    # activities_id_list = form.activities.choice
    activities_id_list = request.form.getlist('activities')
    # activities_id_list_2 = form.activities.choices

    # if form.validate_on_submit():

    ## Create the Trip
    model.create_trip(user_id=user.id, name=trip_name, start_date=start_date, end_date=end_date) # add DESTINATION
    trip = model.get_trip_by_name(trip_name)

## Create the Trip Activity --- later account for multiple activities
    if len(activities_id_list) >= 0:
        model.create_many_trip_activities(trip_id=trip.id, activities_id_list=activities_id_list)
        # pdb.set_trace()
        activity_list = model.get_activities_from_list(activities_id_list=activities_id_list)

# Create the Packing List
    model.create_packinglist(user_id=trip.user_id, trip_id=trip.id)
    # packing_list = model.session.query(PackingList).filter_by(trip_id=trip.id).first()

    return redirect(url_for("packing_list", trip_name=trip_name, trip=trip, activity_list=activity_list, start_date=start_date, end_date=end_date))
    # else:
    #     flash("Field's must be filled!")
    #     return render_template("new_trip.html")

@app.route("/trip/<trip_name>")
@login_required
def packing_list(trip_name):
    trip = model.get_trip_by_name(trip_name)
    # trip_activity_list = model.session.query(TripActivity).filter_by(trip_id=trip.id).all()
    activity_list = model.get_activities_by_trip(trip.id)
    list_of_items = model.get_list_of_items()

    return render_template("packing_list.html", list_of_items=list_of_items, trip=trip,  activity_list=activity_list, trip_name=trip_name, start_date=trip.start_date, end_date=trip.end_date)  # trip_activity_list=trip_activity_list,


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/logout")
def logout():
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



#### Color scheme for background image---- PHOTOSHOP and DESATURATE to make the arrows not so link like!!!!









