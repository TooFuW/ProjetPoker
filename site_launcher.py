from flask import Flask, render_template, request, redirect, flash, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from models import db, User

base_dir = os.path.abspath(os.path.dirname(__file__))

user_db_path = os.path.join(base_dir, 'users.db')

app = Flask(__name__)

dossier_actuel = os.path.dirname(__file__)

app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{user_db_path}'  # Utilisation d'une Base de donnees SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # ... (le reste de votre code pour le traitement de l'inscription)
        return render_template('registration.html')


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        # ... (le reste de votre code pour le traitement de la connexion)
        return render_template('connexion.html')


@app.route('/', methods=['GET', 'POST'])
def accueil():
    title = "MWTE Official Website"
    current_year = 2023
    return render_template('mwte_website.html', title=title, current_year=current_year)


@app.route('/apropos')
def apropos():
    
    return render_template('Apropos.html')


@app.route('/jeux')
def jeux():
    return render_template('Jeux.html')


@app.route('/updates')
def updates():
    return render_template('Update.html')


@app.route('/contact')
def contact():
    return render_template('Contact.html')


@app.route('/merch')
def merch():
    return render_template('Merch.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
