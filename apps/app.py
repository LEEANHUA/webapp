from flask import Flask
from apps.config import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import Rule
import os

db = SQLAlchemy()

app = Flask(__name__)

# 全てのURLにprefixを追加するための処理
APP_ROOT = os.getenv("APP_ROOT")
if not APP_ROOT is None:
    # define custom_rule class
    class Custom_Rule(Rule):
        def __init__(self, string, *args, **kwargs):
            # check endswith '/'
            if APP_ROOT.endswith('/'):
                prefix_without_end_slash = APP_ROOT.rstrip('/')
            else:
                prefix_without_end_slash = APP_ROOT
            # check startswith '/'
            if APP_ROOT.startswith('/'):
                prefix = prefix_without_end_slash
            else:
                prefix = '/' + prefix_without_end_slash
            super(Custom_Rule, self).__init__(prefix + string, *args, **kwargs)

    # set url_rule_class
    app.url_rule_class = Custom_Rule

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