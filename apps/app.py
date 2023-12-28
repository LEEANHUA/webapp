from flask import Flask

app = Flask(__name__)

from apps.processor import views as processor_views

app.register_blueprint(processor_views.processor)

if __name__ == "__main__":
    app.run(debug=True)