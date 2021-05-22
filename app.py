import os
import sys
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
        except Exception as err:
            error_code = getattr(err, "code", 500)
            print("Service exception: ", err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            if hasattr(err, 'message'):
                # python2
                r = json.dumps({"message": err.message, "error_code": error_code})
            else:
                # python3
                r = json.dumps({"message": str(err), "error_code": error_code})
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


@app.route("/tables/<table>", methods=['GET', 'POST'])
@exception_handler
def tables(table, pagination=1):
    pagination = request.args.get('pag', default=pagination, type=int)
    qtd_rows = 100 if pagination == 1 else 10
    if table == 'authors':
        table_name = 'authors'
        table_file = 'tables.html'
        obj = Authors.query.order_by(Authors.author_name.asc()).limit(qtd_rows).all()
    # print(table, table_name, table_file, pagination, qtd_rows)
    return render_template(table_file, table=obj, table_name=table_name, pagination=pagination)


@app.route("/tables/add/<table>", methods=['GET', 'POST'])
@exception_handler
def tables_add(table):
    if table == 'authors':
        table_name = 'authors'
        table_file = 'tables_add.html'

    if request.method == 'POST':
        if table == 'authors':
            obj = Authors(author_id=request.form["author_id"], author_name=request.form["author_name"])
        db.session.add(obj)
        db.session.commit()
        return redirect(url_for('tables/' + table))
    # print(table)

    return render_template(table_file, table_name=table_name)


@app.route("/tables/edit/<table>", methods=['GET', 'POST'])
@exception_handler
def tables_edit(table):
    if table == 'authors':
        obj = Authors.query.get(id)
        table_name = 'authors'
        table_file = 'tables_edit.html'

    if request.method == 'POST':
        if table == 'authors':
            obj.author_id = request.form["author_id"]
            obj.author_name = request.form["author_name"]
        db.session.commit()
        return redirect(url_for('tables.html/' + table))
    # print(table)

    return render_template(table_file, table=obj, table_name=table_name)



@app.route("/tables/delete/<table>/<int:id>", methods=['GET', 'POST'])
@exception_handler
def tables_delete(table, id):
    if table == 'authors':
        obj = Authors.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('tables/' + table))
    print(table)


@app.route("/authors/", methods=['GET'])
@exception_handler
def get_authors():
    authors_obj = Authors.query.all()
    authors_json = [author.to_json() for author in authors_obj]
    return get_response(200, "authors", authors_json, "ok")


@app.route("/author/<int:id>", methods=['GET'])
@exception_handler
def get_author(id):
    author_obj = Authors.query.filter_by(author_id=id).first()
    author_json = author_obj.to_json()
    return get_response(200, "author", author_json, "ok")


@app.route("/author/", methods=['POST'])
@exception_handler
def set_author():
    body = request.get_json()
    author = Authors(author_id=body["author_id"], author_name=body["author_name"])
    db.session.add(author)
    db.session.commit()
    return get_response(201, "author", author.to_json(), "Criado com sucesso")


@app.route("/author/<int:id>", methods=['PUT'])
@exception_handler
def put_author(id):
    author_obj = Authors.query.get(id)
    body = request.get_json()

    if 'author_name' in body:
        author_obj.author_name = body['author_name']

    db.session.add(author_obj)
    db.session.commit()

    return get_response(200, "author", author_obj.to_json(), "Atualizado com sucesso")



@app.route("/author/<int:id>", methods=['DELETE'])
@exception_handler
def del_author(id):
    author_obj = Authors.query.get(id)

    db.session.delete(author_obj)
    db.session.commit()

    return get_response(200, "author", author_obj.to_json(), "Deletado com sucesso")


@app.route("/categories/", methods=['GET'])
@exception_handler
def get_categories():
    categories_obj = Categories.query.all()
    categories_json = [categorie.to_json() for categorie in categories_obj]
    return get_response(200, "categories", categories_json, "ok")


@app.route("/categorie/<int:id>", methods=['GET'])
@exception_handler
def get_categorie(id):
    categorie_obj = Categories.query.filter_by(category_id=id).first()
    categorie_json = categorie_obj.to_json()
    return get_response(200, "categorie", categorie_json, "ok")


@app.route("/formats/", methods=['GET'])
@exception_handler
def get_formats():
    formats_obj = Formats.query.all()
    formats_json = [format.to_json() for format in formats_obj]
    return get_response(200, "formats", formats_json, "ok")


@app.route("/format/<int:id>", methods=['GET'])
@exception_handler
def get_format(id):
    format_obj = Formats.query.filter_by(format_id=id).first()
    format_json = format_obj.to_json()
    return get_response(200, "format", format_json, "ok")


@app.route("/datasets/", methods=['GET'])
@exception_handler
def get_datasets():
    dataset_obj = Dataset.query.all()
    dataset_json = [data.to_json() for data in dataset_obj]
    return get_response(200, "datasets", dataset_json, "ok")


@app.route("/dataset/<int:id>", methods=['GET'])
@exception_handler
def get_dataset(id):
    dataset_obj = Dataset.query.filter_by(id=id).first()
    dataset_json = dataset_obj.to_json()
    return get_response(200, "dataset", dataset_json, "ok")


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
