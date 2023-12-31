from flask import Flask
from apps.config import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config.from_object(config["testing"])

db.init_app(app)
Migrate(app, db)

from apps.guide import views as guide_views

app.register_blueprint(guide_views.guide)

from apps.processor import views as processor_views

app.register_blueprint(processor_views.processor, url_prefix="/processor")

if __name__ == "__main__":
    app.run(debug=True)