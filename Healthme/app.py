import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash

app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


def connect_to_db():



def execute_query(query):
    conn, c = connect_to_db()
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
        enregistrement = request.form['enregistrement']

        # Verifier si tous les champs sont remplis
        if pseudo == "" or sex == "" or dtNaissance == "" or intolerance == "" or allergie == "" or email == "" or motDePass == "":
            return render_template("Inscription.html", error="Veuillez remplir tous les champs")


        # ------------------------------- Vérification l'adresse email est Unique --------------------------------------
        # Vérifier que l'adresse électronique de l'utilisateur existe déjà dans la base de données.
        # L'adresse électronique de l'utilisateur doit être unique en tant que nom de compte pour la connexion.
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
        conn = cx_Oracle.connect(user='PH', password='123456', dsn=dsn_tns)

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
        if enregistrement == "oui":



        # save the user's info to database (if he wants)
        # selon le type de syptome, chercher le type de recette et chercher le type de aliment
        # Créer un écran de confirmation, puis passer à l'écran qui doit être affiché.
        return redirect(url_for('page_confirmation'))

    # page d'inscription
    return render_template("Inscription.html")


# run-------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
