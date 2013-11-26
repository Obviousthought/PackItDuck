##############################################################

# model.py 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import correlation

ENGINE = create_engine("sqlite:///ratings.db", echo= False)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

	#### classes/objects/content goes here


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()


###############################################################

# judgement.py 

from flask import Flask, render_template, redirect, request, url_for, flash, session
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

	#### content #######


if __name__ == "__main__":
    app.run(debug = True)


################################################################

# index.html

{% extends 'master.html' %}
{% block body %}
<form class="signin" method="POST">
    <h2 class="signin-heading">Please sign in</h2>
    <ul>
        {% for message in get_flashed_messages() %}
            <li>{{ message }}</li>
        {% endfor %}
    </ul>
    <input type="text" class="form-control" placeholder="Email" name="email">
    <input type="password" class="form-control" placeholder="Password" name="password">
    <a href="/register">Register a new account</a>
    <input type="submit" class="btn btn-lg btn-primary btn-block" value="Submit">
</form>
{% endblock %}

################################################################

#### Register page #####

# from judgement.py 

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def make_new_user():
    email = request.form.get("email")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    password = request.form.get("password")
    verify_password = request.form.get("password_verify")
    
    if password != verify_password:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    if model.userExists(email):
        flash("Account already exists for user email") 
        return redirect(url_for("register"))

    model.make_new_user(email, password, age, zipcode)
    flash("You've successfully made an account!")
    return redirect(url_for("index"))


# model.py

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable= True)
    password = Column(String(64), nullable= True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable = True)

    ## 

def make_new_user(email, password, age, zipcode):
    new_user = User(email=email, password=password, age=age, zipcode=zipcode)
    session.add(new_user)
    session.commit()



# login/authenticate using flask-peewee for views.py

from flask_peewee.auth import Auth
from flask_peewee.db import Database
from config import db

auth = Auth(app, db, user_model=User)



### Datetime Format for views.py
def format_datetime(date, fmt='%c'):
    # check whether the value is a datetime object
    if not isinstance(date, (datetime.date, datetime.datetime)):
        try:
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception, e:
            return date
    return date.strftime(fmt)

app.jinja_env.filters['datetime'] = format_datetime



### Views.py def index():
    if auth.get_logged_in_user():
        username = current_user.username
        return redirect(url_for("profile", username=username))
    else:
        return render_template("index.html")



