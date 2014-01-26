import flask
from flask import Flask, escape
# from flask.ext.wtf import wtf
# from wtf import DateField, DateTimeField
# # from flask.ext.wtf import DateField, DateTimeField
# from forms import DateField, DateTimeField
import model
from skaffold import Skaffold


app = Flask(__name__)
app.config.from_object(__name__)

Skaffold(app, model.User, model.session)
Skaffold(app, model.Trip, model.session)
Skaffold(app, model.PackingList, model.session)
Skaffold(app, model.PackListItem, model.session)
Skaffold(app, model.Item, model.session)
Skaffold(app, model.ActivityItem, model.session)
Skaffold(app, model.Activity, model.session)
Skaffold(app, model.TripActivity, model.session)

if __name__ == "__main__":
	app.run(host="0.0.0.0")
