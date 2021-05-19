import os
from flask import Flask, url_for, send_from_directory

app = Flask(__name__)


@app.route("/")
def root():
    html = "<h1>Respostas do Teste" \
        "<p>" \
            "Qual a quantidade total de livros da base?</br>" \
            "Qual a quantidade de livros que possuí apenas 1 autor?</br>" \
            "Quais os 5 autores com a maior quantidade de livros?</br>" \
            "Qual a quantidade de livros por categoria?</br>" \
            "Quais as 5 categorias com a maior quantidade de livros?</br>" \
            "Qual o formato com a maior quantidade de livros?</br>" \
            "Considerando a coluna “bestsellers-rank”, quais os 10 livros mais bem posicionados?</br>" \
            "Considerando a coluna “rating-avg”, quais os 10 livros mais bem posicionados?</br>" \
            "Quantos livros possuem “rating-avg” maior do que 3,5?</br>" \
            "Quantos livros tem data de publicação (publication-date) maior do que 01-01-2020?" \
        "</p>"
    return html


# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True)