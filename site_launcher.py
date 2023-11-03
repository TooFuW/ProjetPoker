from flask import Flask, render_template, request, redirect, flash
import os
from flask_sqlalchemy import SQLAlchemy


from models import db, User

base_dir = os.path.abspath(os.path.dirname(__file__))

user_db_path = os.path.join(base_dir, 'users.db')

app = Flask(__name__)



app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{user_db_path}'  # Utilisation d'une Base de donnees SQLite


db.init_app(app)





@app.route('/registration', methods=['GET', 'POST'])

def registration():
    
    #On recupere les informations rentrees par l'utilisateur dans le formulaire HTML
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        prenom = request.form['prenom']
        nom = request.form['nom']
        genre = request.form['genre']
        

        # Vérifiez si l'utilisateur existe déjà dans la base de données
        existing_user = User.query.filter_by(email=email,username=username).first()
        if existing_user:
            flash('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.', 'danger')
        else:
            # Cree un nouvel utilisateur et l ajoute a la base de donnees
            new_user = User ( username = username , email = email , password = password , prenom = prenom ,
    nom = nom , genre = genre )

            db.session.add(new_user)
            db.session.commit()
            flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
            return redirect('/')
    return render_template('registration.html')




@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérification de l'adresse email et du mot de passe dans la base de données
        utilisateur = User ( username = username , password = password )
        if utilisateur:
            # Redirection vers une page de succès ou autre (connexion réussie)
            flash('Connexion réussie!', 'success')
            return redirect('/')
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect. Veuillez réessayer.", 'danger' )


    return render_template('connexion.html')



@app.route('/', methods=['GET', 'POST'])
def accueil():
    title = "Site de Vente de Produits"
    current_year = 2023

    return render_template('Template Site MWTE\mwte_website.html', title=title, current_year=current_year)


if __name__ == '__main__':


    with app.app_context():
        db.create_all()
    app.run(debug=True)
