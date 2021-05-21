import os
import simplejson as json
from dataclasses import dataclass
from datetime import datetime
from flask import Flask, url_for, send_from_directory, render_template, request, redirect, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import *
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = SQLAlchemy(app)


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_code = getattr(e, "code", 500)
            print("Service exception: %s", e)
            if hasattr(e, 'message'):
                # python2
                r = json.dumps({"message": e.message, "error_code": error_code})
            else:
                # python3
                r = json.dumps({"message": str(e), "error_code": error_code})
            return Response(r, status=error_code, mimetype='application/json')

    # Renaming the function name:
    wrapper.__name__ = func.__name__
    return wrapper


def get_response(status, content_title, content, mensage=False):
    body = {}
    body[content_title] = content
    body_json = json.dumps(body, use_decimal=True, encoding='utf-8', default=str)

    if mensage:
        body['mensage'] = mensage

    return Response(body_json, status=status, mimetype="application/json")


@app.route("/", methods=['GET', 'POST'])
@exception_handler
def root():
    return render_template('index.html')


@app.route("/authors/", methods=['GET'])
@exception_handler
def authors():
    authors_obj = Authors.query.all()
    authors_json = [author.to_json() for author in authors_obj]
    return get_response(200, "authors", authors_json)


@app.route("/categories/")
@exception_handler
def categories():
    categories_dict = Categories.query.all()
    categories_json = [categorie.to_json() for categorie in categories_dict]
    return get_response(200, "categories", categories_json)


@app.route("/formats/")
@exception_handler
def formats():
    formats_dict = Formats.query.all()
    formats_json = [format.to_json() for format in formats_dict]
    return get_response(200, "formats", formats_json)


@app.route("/dataset/")
@exception_handler
def dataset():
    dataset_dict = Dataset.query.all()
    dataset_json = [data.to_json() for data in dataset_dict]
    return get_response(200, "dataset", dataset_json)


# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('server_error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
