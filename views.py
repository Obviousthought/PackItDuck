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
    # trips = Trip.query.all()

    if session.get('id'):
        user_id = session['id']
        user = model.get_user_by_id(user_id)
        return redirect(url_for("profile", user_id=user_id))
    else:
        return render_template("index.html")


    # user_id = session.get('id')
    # if user_id == None:
    #   return render_template("index.html")
    # else:
    #   user = model.get_user_by_id(user_id)
    #   profile_link = my_profile_link()
    #   return redirect(url_for("profile", user_id=user_id, profile_link=profile_link))

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
        return redirect(url_for("profile", user_id=user.id))

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
    flash("You've successfully made an account!")

    user_id = session.get('id')
    user = model.get_user_by_id(user_id)
    id = session.get('id')

    return redirect(url_for("profile", user_id=user.id))

def my_profile_link():
    if session.get('id'):
        profile_link = session['id']
    else:
        profile_link = None
    return profile_link

@app.route("/profile/<user_id>")
# @login_required
def profile(user_id):
    profile_link = my_profile_link()
    user = model.get_user_by_id(user_id)

    packlist_id = model.get_user_packlist(user_id)
    # trip_name = model.get_user_trips(user_id)

    return render_template("home_page.html", user_id=user_id, username=user.username, packlist_id=packlist_id, email=user.email, profile_link=profile_link)

# @app.route("/profile/<user_id>/<")


@app.route("/profile/trip")
@login_required
def create_trip():
    form = forms.NewTripForm(request.form)
    if not form.validate():
        flash("All fields must be filled!")
        return render_template("new_trip.html")

    trip = Trip(name=form.name.data, start_date=form.start_date.data, end_date=form.end_date.data)
    current_user.trips.append(trip)



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













