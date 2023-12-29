from flask import Flask
from apps.config import config

app = Flask(__name__)

app.config.from_object(config["local"])

from apps.guide import views as guide_views

app.register_blueprint(guide_views.guide)

from apps.processor import views as processor_views

app.register_blueprint(processor_views.processor, url_prefix="/processor")

if __name__ == "__main__":
    app.run(debug=True)