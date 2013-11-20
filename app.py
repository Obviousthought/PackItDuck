import flask
from flask import Flask, escape
# from flask.ext.wtf import DateField, DateTimeField
import model
# from skaffold import Skaffold

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config.from_object(__name__)

# Skaffold(app, model.User, model.session)
# Skaffold(app, model.Trip, model.session)
# Skaffold(app, model.PackingList, model.session)
# Skaffold(app, model.PackListItem, model.session)
# Skaffold(app, model.Item, model.session)
# Skaffold(app, model.ActivityItem, model.session)
# Skaffold(app, model.Activity, model.session)

if __name__ == "__main__":
	admin = Admin(app)
	admin.add_view(ModelView(model.User, model.session))
	admin.add_view(ModelView(model.Trip, model.session))
	admin.add_view(ModelView(model.PackingList, model.session))
	admin.add_view(ModelView(model.PackListItem, model.session))
	admin.add_view(ModelView(model.Activity, model.session))
	admin.add_view(ModelView(model.Item, model.session))
	admin.add_view(ModelView(model.TripActivity, model.session))
	admin.add_view(ModelView(model.ActivityItem, model.session))
	app.run()
