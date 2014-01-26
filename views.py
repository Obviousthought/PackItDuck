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
import json
import forecastio
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
    # packlist_id = model.get_user_packlist(user.id)
    # trip_names = model.get_user_trip_names(user.id)
    trip_list = model.get_user_trips(user.id)

    # packlist_items = []
    # for trip in trip_list:
    #     packing_list = model.session.query(PackingList).filter_by(trip_id=trip.id).first()
    #     # packing_list_id = model.session.query(PackingList).filter_by(trip_id=trip.id).get(id)
    #     packlist_item = model.session.query(PackListItems).filter_by(packing_list_id=packing_list.id).first()
    #     packlist_items.append(packlist_item.id)

    # attr_packlist_items = []
    # for item in packlist_items:
    #     item_name = model.session.query(Item).filter_by(id=item).get(name)
    #     item_qty = model.session.query(PackListItems).filter_by(item_id=item).get(item_qty)
    #     attr_packlist_items.append(item_name, item_qty)

    return render_template("home_page.html", user_id=user.id, username=user.username, trip_list=trip_list) #, packlist_id=packlist_idpacklist_items=packlist_items


@app.route("/new_trip")
@login_required
def new_trip():
    form = forms.NewTripForm(request.form)
    form.activity.choices = [(act.id, act.name) for act in Activity.query.order_by('name')]
    if not form.validate():
        return render_template('new_trip.html', form=form)
    else:
        return redirect(url_for('create_trip'))

    # activities = model.session.query(Activity).all()
    # return render_template("new_trip.html", activities=activities)

@app.route("/new_trip", methods=["GET", "POST"])
@login_required
def create_trip():
    user = current_user
    form = forms.NewTripForm(request.form)

    trip_name = request.form.get("name")
    destination = request.form.get("destination")
    start_date= request.form.get("start_date")
    end_date= request.form.get("end_date")
    activity_id = request.form.get("activity")

## Create the Trip
    model.create_trip(user_id=user.id, destination=destination, name=trip_name, start_date=start_date, end_date=end_date)
    trip = model.get_trip_by_name(trip_name)

## Create the Trip Activity --- later account for multiple activities        
    activity = model.session.query(Activity).filter_by(id=activity_id).first()
    model.create_trip_activity(trip_id=trip.id, activity_id=activity.id)

# Create the Packing List
    model.create_packinglist(user_id=trip.user_id, trip_id=trip.id)
    packing_list = model.get_packlist_by_trip(trip.id)

# Filter/Create PackListItems:
    packlist_items = []

    db_item_list = model.session.query(Item).all()
    if len(packlist_items) == 0:
        for item in db_item_list:
            if item.always != None:
                packlist_items.append(item.id)
        # return packlist_items

    # if trip.total_days >= 1:
    #     for item in packlist_items:
    #         item_qty = trip.total_days - 1
    #         model.update_item_qty(packing_list_id=packing_list.id, item_id=item, item_qty=item_qty)

# Create Pack List Items
    model.create_packlist_item(packing_list_id=packing_list.id, packlist_items=packlist_items, total_days=trip.total_days)

# Update Pack List Items with Activity Items
    activity_pl_items = []

    if activity.id != 12:
        activity_items = model.session.query(ActivityItem).filter_by(activity_id=activity.id).all()
        for act_item in activity_items:
            if activity.id == act_item.activity_id:
                activity_pl_items.append(act_item.item_id)
                packlist_items.append(item.id)               

    model.add_activity_item(packing_list_id=packing_list.id, act_pl_items=activity_pl_items)

# on model.py change create_packlist_item to take in a list of items and the packing_list_id
    # model.create_packlist_item(packing_list_id=packing_list.id)

    return redirect(url_for("packing_list", trip_name=trip.name, packlist_items=packlist_items, trip=trip, packing_list=packing_list, destination=trip.destination, activity=activity, start_date=trip.start_date, end_date=trip.end_date)) # activity_list=activity_list


@app.route("/trip/<trip_name>")
@login_required
def packing_list(trip_name):
    trip = model.get_trip_by_name(trip_name)
    activity_list = model.get_activities_by_trip(trip.id)
    # list_of_items = model.get_list_of_items()

    # packlist_items = []

    packing_list = model.session.query(PackingList).filter_by(trip_id=trip.id).first()

    packlist_items = model.session.query(PackListItems).filter_by(packing_list_id=packing_list.id).all()

    attr_packlist_items = []
    for item in packlist_items:
        item_qty = item.item_qty
        i = model.session.query(Item).filter_by(id=item.item_id).first()
        item_name = i.name
        attr_packlist_items.append((item_name, item_qty))


    # for list_item in packing_list.packlist_items:
    #     packlist_items.append(list_item.id)

    # for list_item in packing_list.packlist_items:
    #     packlist_items.append(list_item.id)

    # attr_packlist_items = []
    # for item in packlist_items:

    #     i = model.session.query(Item).filter_by(id=item).first()
        
    #     # pdb.set_trace()
    #     if not i:
    #         #handle missing item item
    #         pass
    #     else:
    #         item_name = i.name

    #         # item_name = model.session.query(Item).filter_by(id=item).name
    #         item_qty = model.session.query(PackListItems).filter_by(item_id=item).count()

    #         attr_packlist_items.append((item_name, item_qty))
    # raise Exception(attr_packlist_items)
    return render_template("packing_list.html", trip=trip, attr_packlist_items=attr_packlist_items,activity_list=activity_list, trip_name=trip_name, start_date=trip.start_date, end_date=trip.end_date)  # trip_activity_list=trip_activity_list,list_of_items=list_of_items


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

# host="0.0.0.0"