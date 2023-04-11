import sqlite3

import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash

app = Flask(__name__,static_folder='static')
app.secret_key = 'my_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


def connect_to_db():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
    conn = cx_Oracle.connect(user='PH', password='123456', dsn=dsn_tns)
    return conn


def execute_query(query):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    return c.fetchall()


# page d'acceuil---------------------------------------------------------------------------
@app.route('/')
def page_acceuil():
    return render_template("Page_acceuil.html")


@app.route('/symptomes')
def symptomes():
    return render_template("symptomes.html")


@app.route("/Aliments")
def aliment():
    return render_template("Aliments.html")


@app.route('/recette')
def recette():
    return render_template("recette.html")


@app.route('/Inscription', methods=["POST", "GET"])
def inscription():
    # recuperer des info de utlisateur
    if request.method == 'POST':
        pseudo = request.form["Pseudo"]
        sex = request.form["sex"]
        dtNaissance = request.form["Dt"]
        intolerance = request.form["intolerance"]

        # Si l'utilisateur choisit "Autres" en 'intolerance'
        if intolerance == "Autres":
            intolerance = request.form["Autre_Intolerance"]
        allergie = request.form['allergie']
        traitement_maladie = request.form['maladie']

        # Si l'utilisateur choisit "Autres" dans la formulaire'
        if traitement_maladie == "Autres":
            traitement_maladie = request.form['Autre_Maladie']

        email = request.form['email']
        motDePass = request.form['motdepass']

        # Si l'utilisateur choisit enregistrer ses informations
        enregistrement = request.form['enregistrement']

        # Verifier si tous les champs sont remplis
        if pseudo == "" or sex == "" or dtNaissance == "" or intolerance == "" or allergie == "" or email == "" or motDePass == "":
            return render_template("Inscription.html", error="Veuillez remplir tous les champs")

        # ------------------------------- Vérification l'adresse email est Unique --------------------------------------
        # Vérifier que l'adresse électronique de l'utilisateur existe déjà dans la base de données.
        # L'adresse électronique de l'utilisateur doit être unique en tant que nom de compte pour la connexion.

        query_existant = f""" 
            select *
            from Client
            where EmailC = {email}
        """

        res_query_existant = execute_query(query_existant)
        # --------------------------------- Flash Messaging System ---------------------------------------------------
        # On utilise Flash pour rendre un message dans le page inscription.
        if res_query_existant:
            flash('Cette adresse e-mail est déjà enregistrée.')
            return redirect('/inscription.html')
        # [Manque] HTML code - block pour recevoir ce message
        # <...>

        # Inscription réussie...
        # ==>
        # Stocker des donnees

        # ------------------------------- Stockage des info --------------------------------------
        # Stocker l'utilisateur dans la base de données'
        # si l'utilisateur choisit "enregistrement", on enregistre ses informations dans la base de donnees
        # avant la insertion, on crypte le mot de passe en utilisant la fonction "Salted Hash" -- (RGBD)
        if enregistrement == "oui":
            # creer "salt"
            salt = bcrypt.gensalt()
            # crypter le mot de passe
            hashed_password = bcrypt.hashpw(motDePass.encode('utf-8'), salt)

            query_insert = f"""
                insert into Client (Pseudo, Sexe, DtNaissance, Intolerance, EmailC, MotDePass)
                values ({pseudo}, {sex}, {dtNaissance}, {intolerance}, {email}, {hashed_password})
            """

            execute_query(query_insert)

        # selon le type de syptome, chercher le type de recette et chercher le type de aliment
        # -------------------------------------- Session ---------------------------------------------------------------
        # mettre les données dans la session
        session['intolerance'] = intolerance
        session['allergie'] = allergie
        session['traitement_maladie'] = traitement_maladie

        # La page de confirmation contient deux boutons,
        # l'un permettant d'accéder à la page recommandée à l'utilisateur
        # et l'autre de revenir à la page d'accueil.
        return redirect(url_for('page_confirmation'))

    # page d'inscription
    return render_template("Inscription.html")


@app.route('/confirmation')
def page_confirmation():
    if request.method == 'POST':
        # Recuperer des info de utlisateur de la session
        if 'intolerance' in session:
            intolerance = session['intolerance']
        if 'allergie' in session:
            allergie = session['allergie']
        if 'traitement_maladie' in session:
            traitement_maladie = session['traitement_maladie']

        # -------------------------------------- Interroger sur la base ------------------------------------------------
        # Chercher le type de recette et le type de aliment sur la base de données
        # On va trouver le recette par rapport a aliments sante
        query_recette = '''
            
        '''

        res_query_recette = execute_query(query_recette)

        return redirect(url_for('recette', recette=res_query_recette))

    return render_template("Page_confirmation.html")


# run-------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
