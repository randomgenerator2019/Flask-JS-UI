'''
Intended to be the main access point for application. Containing endpoints for frontend
'''

#- standard library imports
import os

#- 3rd party library imports
from flask import Flask, render_template, request, url_for, redirect
import flask_monitoringdashboard as dashboard
import backend.html as html
# please note the API version numbers.
from blueprints.api_v1 import blueprint

# quick and dirty Flask config
template_dir = os.path.join(os.getcwd(), "templates")
static_dir = os.path.join(os.getcwd(), "static")
views = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

# disable caching
views.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1
views.config.SWAGGER_UI_OPERATION_ID = True
views.config.SWAGGER_UI_REQUEST_DURATION = True

# Attach API blueprint note this is redirected to /api/v1
views.register_blueprint(blueprint)

# Attach Flask-monitoring dashboard
# source https://flask-monitoringdashboard.readthedocs.io/en/master/configuration.html
dashboard.config.init_from(file='blueprints/monitoring.cfg')
dashboard.bind(views)

#-----------
# Views
#-----------

@views.after_request
def add_header(response):
    '''
    Disable caching
    '''
    response.headers['Cache-Control'] = 'no-store'
    return response


@views.route("/")
def home():
    '''
    Render index.html
    '''
    return render_template("index.html", html=html)

@views.route("/widgets")
def widgets():
    '''
    Render index.html
    '''
    return render_template("widgets.html", html=html)


def run_views():
    views.run(host="127.0.0.1", port=5000, threaded=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Flask Views')
    parser.add_argument('-d', '--debug', help='debug', required=False)
    args = parser.parse_args()
    if args.debug == "True":
        print("###ENDPOINTS###\n{}\n#############".format(views.url_map))
        views.run(host="127.0.0.1", port=5000, threaded=True, debug=True)
    else:
        run_views()
