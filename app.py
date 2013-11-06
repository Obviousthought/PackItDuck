from flask import Flask
import model
from skaffold import Skaffold

app = Flask(__name__)
app.config.from_object(__name__)

Skaffold(app, model.User, model.session)
Skaffold(app, model.Movie, model.session)

if __name__ == "__main__":
    app.run()
