from flask import Flask, render_template, redirect, request, g, session, url_for, flash
from model import User
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
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)

@app.route("/")
def index():
    if session.get("id"):
        user = model.user_by_id(session["id"])
        return redirect(url_for("profile", user_id.id))
    else:
        return render_template("index.html", user_id=None)

@app.route("/", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("index.html")

    username = form.username.data
    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("index.html")

    login_user(user)
    return redirect(request.args.get("next", url_for("profile")))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def create_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    verify_password = request.form.get("password_verify")
    
    if password != verify_password:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    if model.userExists(email):
        flash("Account already exists for user email") 
        return redirect(url_for("register"))

    model.create_user(username, email, password)
    flash("You've successfully made an account!")
    return redirect(url_for("index"))

@app.route("/clear")
def clear_session():
    session.clear()
    return redirect(url_for("index"))

@app.route("/profile/<user_id>")
def user_profile(user_id):
    profile_link = my_profile_link()
    user = model.user_by_id(user_id)
    trips = model.get_trip_list(user_id)
    if session.get('id'):
        if session['id'] == int(user_id):
            return render_template("profile.html", user_id=user_id, email = user.email, 
                                    movie_ratings=movie_ratings, profile_link=profile_link)
        else:
            return render_template("user_profile.html", user_id=user_id, email = user.email, 
                        movie_ratings=movie_ratings, profile_link=profile_link)
    else:
        return render_template("user_profile.html", user_id=user_id, email = user.email, 
                        movie_ratings=movie_ratings, profile_link=profile_link)



if __name__ == "__main__":
    app.run(debug=True)
