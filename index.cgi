#!/home/miyamoto/public_html/webapp/venv_webapp/bin/python3
import cgitb
cgitb.enable()
from wsgiref.handlers import CGIHandler
from apps.app import app
CGIHandler().run(app)
