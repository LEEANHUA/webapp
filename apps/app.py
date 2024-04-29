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

# 外部からのアクセスを許可するためには、debug=Falseとし、hostを設定する必要がある
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')