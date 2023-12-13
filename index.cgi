#!/home/miyamoto/public_html/webapp/venv_webapp/bin/python3
import cgitb
cgitb.enable()
from wsgiref.handlers import CGIHandler
from app import app
CGIHandler().run(app)
