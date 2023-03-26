from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3, os, datetime

def connect_to_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    return conn, c

def excute_query(query):
    conn, c = connect_to_db()
    c.execute(query)
    conn.commit()
    conn.close()
    return c.fetchall()


app = Flask(__name__)

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
        Pseudo = request.form["Pseudo"]
        Sexe = request.form["sexe"]
        DtNaissance = request.form["Dt"]
        Intolerane = request.form["intolerance"]
        # Si l'utilisateur choisit
        if Intolerane == "Autres":
            Intolerane = request.form["Autre_Intolerance"]
        Allergie = request.form['allergie']
        traitement_maladie = request.form['maladie']
        # Si l'utilisateur choisit autre dans la formulaire'
        if traitement_maladie == "Autres":
            traitement_maladie = request.form['Autre_Maladie']
        Email = request.form['email']
        MotDePass = request.form['motdepass']
        enregistrement = request.form['enregistrement'

        # si l'utilisateur choisit enregistrement, on enregistre ses informations dans la base de donnees
        if enregistrement == "oui":
            enregistrement = "1"
        else:
            enregistrement = "0"

        # Verifier si tous les champs sont remplis
        if Pseudo == "" or Sexe == "" or DtNaissance == "" or Intolerane == "" or Allergie == "" or Email == "" or MotDePass == "":
            return render_template("Inscription.html", error="Veuillez remplir tous les champs")

        # Verifier si l'utilisateur existe dans la base de données'
        query_existant = f"""
            select *
            from Client
            where EmailC = {Email}
        """

        existant = excute_query(query_existant)
        if len(existant) > 0:
            return render_template("Inscription.html", error="Cet utilisateur existe déjà")

        

        # Stocker l'utilisateur dans la base de données'
        user = {'useremail': Email, 'MotDePass': MotDePass}
        users.append(user)
        session['useremail'] = Email

        # save the user's info to database (if he wants)
        # selon le type de syptome, chercher le type de recette et chercher le type de aliment
        # Créer un écran de confirmation, puis passer à l'écran qui doit être affiché.
        return redirect(url_for('page_confirmation'))

    return render_template("Inscription.html")


# run-------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
