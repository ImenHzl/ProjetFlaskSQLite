from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session admin
def est_authentifie():
    return session.get('authentifie')

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie_user():
    return session.get('authentifieUser')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return render_template('recherche.html')

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)


@app.route('/authentificationUser', methods=['GET', 'POST'])
def authentificationUser():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['authentifieUser'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('recherche_nom'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentificationUser.html', error=True)

    return render_template('formulaire_authentificationUser.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

@app.route('/fiche_nom/', methods=['GET', 'POST'])
def recherche_nom():
    error_message = None
    data = None
    if not est_authentifie_user():
        # Rediriger vers la page d'authentification utilisateur si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentificationUser'))
    
    if request.method == 'POST':
        nom = request.form['nom']
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Utiliser sqlite3.Row pour obtenir des résultats sous forme de dictionnaire
        cursor = conn.cursor()
        cursor.execute('SELECT nom, prenom, adresse FROM clients WHERE nom = ?', (nom,))
        data = cursor.fetchone()
        conn.close()
        if not data:
            error_message = "Nom non trouvé dans la base de données."
    return render_template('read_nom.html', data=data, error_message=error_message)
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
