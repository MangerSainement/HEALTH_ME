from datetime import datetime
from translate import Translator

import cx_Oracle
import bcrypt
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort

app = Flask(__name__, static_folder='static')
app.secret_key = 'my_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


def connect_to_db():
    dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='XE')
    conn = cx_Oracle.connect(user='C##PH', password='123456', dsn=dsn_tns)
    print('Connecting to database')
    return conn


def execute_query(query):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(query)
    res = c.fetchall()
    conn.commit()
    conn.close()
    print('Executing query')
    return res


def execute_insert(query):
    conn = connect_to_db()
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    print('insert!')


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


@app.route('/resultat')
def resultat():
    return render_template("resultat.html")


@app.route("/aliment&recette")
def cliquer_symptome():
    return render_template("symptome_cliquer.html")


@app.route('/Inscription', methods=["POST", "GET"])
def inscription():
    # recuperer des info de utlisateur
    if request.method == 'POST':
        pseudo = request.form["Pseudo"]
        sex = request.form["sexe"]
        dtNaissance = request.form["Dt"]

        email = request.form['email']
        motDePass = request.form['motdepass']

        # noveau !
        symptome = request.form['symptome']
        # print(symptome)
        # print(pseudo)
        # print(sex)
        # print(dtNaissance)
        # print(email)
        # print(motDePass)

        # Si l'utilisateur choisit enregistrer ses informations
        enregistrement = request.form['enregistrement']

        # Verifier si tous les champs sont remplis
        if pseudo == "" or sex == "" or dtNaissance == "" or email == "" or motDePass == "":
            return render_template("Inscription.html", error="Veuillez remplir tous les champs")

        # ------------------------------- Vérification l'adresse email est Unique --------------------------------------
        # Vérifier que l'adresse électronique de l'utilisateur existe déjà dans la base de données.
        # L'adresse électronique de l'utilisateur doit être unique en tant que nom de compte pour la connexion.

        query_existant = f""" 
            select *
            from Client
            where EmailC = '{email}'
        """

        res_query_existant = execute_query(query_existant)
        print(res_query_existant)
        # --------------------------------- Flash Messaging System ---------------------------------------------------
        # On utilise Flash pour rendre un message dans le page inscription.
        if res_query_existant:
            flash('Cette adresse e-mail est déjà enregistrée.')
            return redirect('/inscription')
        # [Manque] HTML code - block pour recevoir ce message
        # <...>

        # Inscription réussie...
        # ==>
        # Stocker des donnees

        # ------------------------------- Stockage des info --------------------------------------
        # Stocker l'utilisateur dans la base de données'
        # si l'utilisateur choisit "enregistrement", on enregistre ses informations dans la base de donnees
        # avant l‘insertion, on crypte le mot de passe en utilisant la fonction "Salted Hash" -- (RGPD)
        print("enregistrement :" + enregistrement)
        if enregistrement == "oui":
            # creer "salt"
            salt = bcrypt.gensalt()

            # crypter le mot de passe
            hashed_password = bcrypt.hashpw(motDePass.encode('utf-8'), salt)

            dtNaissance = datetime.strptime(dtNaissance, '%Y-%m-%d')
            dtNaissance = dtNaissance.strftime('%d/%m/%Y')

            hashed_password = hashed_password.decode('utf-8')
            salt = salt.decode('utf-8')

            query_insert = f"""
                insert into Client (Pseudo, Sexe, DateAnniversaieC, EmailC, MOTDEPASSE, STORED_SALT)
                values ('{pseudo}', '{sex}', to_date('{dtNaissance}', 'DD/MM/YYYY'), '{email}', '{hashed_password}', '{salt}')
            """

            execute_insert(query_insert)

            # Maintenat, il faut trouver CodeC pour insert le donnees
            # (Client a quel syptome, et quel detester ou allergie)
            query_GetCodeC = f"""
                select CodeC 
                from client
                where EMAILC = '{email}'
            """

            CodeC = execute_query(query_GetCodeC)
            CodeC = CodeC[0][0]

            # Cherche le code de le symptome
            query_CodeS = f"""
                select CodeS
                from SYMPTOMES
                where NOMS = '{symptome}'
            """

            CodeS = execute_query(query_CodeS)
            CodeS = CodeS[0][0]

            # Faire l'insertion de la table d'AVOIR
            query_Avoir = f"""
                            insert into AVOIR(CodeC, CodeS)
                            values ({CodeC}, {CodeS})
                        """

            execute_insert(query_Avoir)
            print('OK')

        # selon le type de syptome, chercher le type de recette et chercher le type de aliment
        # -------------------------------------- Session ---------------------------------------------------------------
        # mettre les données dans la session
        print(symptome)
        session['symptome'] = symptome
        session['email'] = email
        session['pseudo'] = pseudo

        # La page de confirmation contient deux boutons,
        # l'un permettant d'accéder à la page recommandée à l'utilisateur
        # et l'autre de revenir à la page d'accueil.
        return redirect(url_for('page_confirmation'))

    # ------------------------page d'inscription-------------------------------------------

    return render_template("Inscription.html")

    # ------------- page connection------------------------------


@app.route('/connecter', methods=["POST", "GET"])
def connecter():
    if request.method == 'POST':
        email = request.form['email']
        motDePass = request.form['motdepass']

        # Verifier l'email et le mot de passe
        error = None
        res = check_user_credentials(email, motDePass)
        if res == 1:
            query_pseudo = f"""
                select PSEUDO
                from CLIENT
                where EMAILC = '{email}'
            
            """

            pseudo = execute_query(query_pseudo)
            session['pseudo'] = pseudo[0][0]
            session['email'] = email
            return redirect(url_for('page_acceuil'))
        elif res == 0:
            error = "Nom d'utilisateur ou mot de passe incorrect"
        elif res == 404:
            error = "L'utilisateur n'existe pas, veuillez vous enregistrer"
        return render_template("connecter.html", error=error)

    return render_template("connecter.html")


def check_user_credentials(email, password):
    # interroger le mot de passe
    query = f"""
            SELECT EmailC, MOTDEPASSE, STORED_SALT 
            FROM Client 
            WHERE EMAILC = '{email}'
            """

    user_data = execute_query(query)

    if user_data:
        email, stored_password, stored_salt = user_data[0][0], user_data[0][1], user_data[0][2]

        # 使用存储的salt对提供的密码进行哈希
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), stored_salt.encode('utf-8'))

        # 检查提供的密码哈希是否与存储的密码哈希匹配
        if hashed_password.decode('utf-8') == stored_password:
            print("1")
            return 1
        else:
            print("0")
            return 0
    else:
        print("404")
        return 404


@app.route('/confirmation', methods=['GET', 'POST'])
def page_confirmation():
    if request.method == 'POST':

        # Recuperer de l'info d'utlisateur de la session
        symptome = session['symptome']

        # -------------------------------------- Interroger sur la base ------------------------------------------------
        # Chercher le type de recette et le type d'aliment sur la base de données
        # On va trouver la recette par rapport à aliments sante

        query_MinerauxSoulager = f'''
                    select MINERAUX.CODEM, MINERAUX.NOMM
                    from SOULAGER, MINERAUX, SYMPTOMES
                    where SOULAGER.CODEM = MINERAUX.CODEM
                    and SYMPTOMES.CODES = SOULAGER.CODES
                    and NomS = '{symptome}'
                '''

        liste_CodeM = execute_query(query_MinerauxSoulager)

        liste_Besoin_Mineraux = []
        liste_Aliment_recommandation = []

        for i in liste_CodeM:
            liste_Besoin_Mineraux.append(i[1])  # Ajouter les minéraux requis à la liste
            i = i[0]  # le code de Mineral

            query_trouverAlimentRecommande = f"""
                SELECT ALIMENTS.CodeA, NOMA, QTEM
                FROM MINERAUX, CONTENIR, ALIMENTS
                WHERE MINERAUX.CODEM = CONTENIR.CODEM
                AND CONTENIR.CODEA = ALIMENTS.CODEA
                AND MINERAUX.CODEM = {i}
                ORDER BY QTEM DESC
            """

            resultat1 = execute_query(query_trouverAlimentRecommande)

            liste_Aliment_recommandation.append(resultat1[0][1])

        return render_template('Page_personnalisée.html',
                               liste=liste_Aliment_recommandation,
                               liste2=liste_Besoin_Mineraux,
                               symptome=symptome)

    return render_template("page_confirmation.html")


@app.route('/aliment_cliquer/<nom>')
def aliment_cliquer(nom):
    translator = Translator(from_lang='french', to_lang='english')
    nom_translation = translator.translate(nom)

    req = execute_query("select NomA from Aliments")
    if nom_translation not in req[0]:
        return abort(404)

    return render_template("aliment_cliquer.html", nom=nom)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('pseudo', None)
    session.pop('symptome', None)
    return redirect(url_for('page_acceuil'))


@app.route('/monCompte', methods=['GET', 'POST'])
def monCompte():
    if request.method == 'POST':
        email = session['email']
        message = ""
        message_MDP = ""
        if request.form["nouveau_pseudo"] != '':
            nouveau_pseudo = request.form['nouveau_pseudo']
            # mise à jour du pseudo dans la base de données
            # alter/insert query remplacer les données dans la base de données
            query_pseudo_changement = f"""
                update CLIENT
                set PSEUDO = '{nouveau_pseudo}'
                where EMAILC = '{email}'
             """

            execute_insert(query_pseudo_changement)

            # verification nouveau_pseudo
            query_pseudo_verification = f"""
                select PSEUDO
                from CLIENT
                where EMAILC = '{email}'
            """

            res_verification = execute_query(query_pseudo_verification)

            if res_verification[0][0] == nouveau_pseudo:
                message = 'Votre pseudo a été modifié !'
                session['pseudo'] = nouveau_pseudo
            else:
                message = 'Veuillez réessayer !'

        if request.form['nouveau_MDP'] != '':
            nouveau_mdp = request.form['nouveau_MDP']
            session['motdepass'] = nouveau_mdp
            # mise à jour du mot de passe dans la base de données
            # alter/insert query remplacer les données dans la base de données

            # creer "salt"
            salt = bcrypt.gensalt()

            # crypter le mot de passe
            hashed_password = bcrypt.hashpw(nouveau_mdp.encode('utf-8'), salt)

            # Conversion de chaînes binaires en chaînes
            hashed_password = hashed_password.decode('utf-8')
            salt = salt.decode('utf-8')

            # Update password
            query_MDP_changement = f"""
                update CLIENT
                set MOTDEPASSE = '{hashed_password}', STORED_SALT = '{salt}'
                where EMAILC = '{email}'
            """

            execute_insert(query_MDP_changement)

            # verification MDP
            query_MDP_verification = f"""
                select MOTDEPASSE
                from CLIENT
                where EMAILC = '{email}'
            """

            res_MDP_verification = execute_query(query_MDP_verification)
            if res_MDP_verification[0][0] == hashed_password:
                message_MDP = 'Votre mot de pass a été modifié !'
            else:
                message_MDP = 'Veuillez réessayer de changer mot de pass !'

        return render_template('Page_confirmation_changement.html', message_MDP=message_MDP, message=message)

    if session['email']:
        email = session['email']

        query_infoCLi = f"""
               select CODEC, PSEUDO, SEXE, DATEANNIVERSAIEC, EMAILC
               from CLIENT
               where EMAILC = '{email}'
           """

        infoCli = execute_query(query_infoCLi)
        infoCli = infoCli[0]
        dt_str = infoCli[3].strftime('%d-%m-%Y')

        print(dt_str)

        infoCLI_dict = {
            "CodeCli": infoCli[0],
            "Pseudo": infoCli[1],
            "gendre": infoCli[2],
            "email": infoCli[4],
        }

        print(infoCLI_dict)

    return render_template('Page_MonCompte.html', info=infoCLI_dict, dt=dt_str)


@app.route('/Page_confirmation_changement', methods=['GET', 'POST'])
def ConfirmationChangement():
    return render_template('Page_confirmation_changement.html')


#  run -----------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
