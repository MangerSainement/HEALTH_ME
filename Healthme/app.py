from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3, os, datetime

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
        Email = request.form['email']
        MotDePass = request.form['motdepass']

    return render_template("Inscription.html")


# run-------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
