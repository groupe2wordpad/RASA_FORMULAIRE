import os
import requests
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'une_clef_secrete_pour_flash'  # nécessaire pour flash messages

# Configuration PostgreSQL (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bdd_entrainement_rasa_user:X4dXXHlehramSkQvDYWAyGoSz9VcnaFW@dpg-d109t40gjchc73agl4c0-a.oregon-postgres.render.com/bdd_entrainement_rasa"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# URL du bot Rasa hébergé sur Render
RASA_URL = "https://referentiel-rasa.onrender.com/webhooks/rest/webhook"

# Modèle Question
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    reponse = db.Column(db.Text, nullable=True)

# Modèle Remarque
class Remarque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texte = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Création des tables (si elles n'existent pas déjà)
with app.app_context():
    db.create_all()

# Route principale : affichage + soumission de question
@app.route("/", methods=["GET", "POST"])
def formulaire():
    question = None
    reponse = None
    message_accueil = "Pose-moi ta question sur moi ou sur la culture Baoulé !"

    if request.method == "POST":
        question = request.form.get("question")
        if question:
            try:
                response = requests.post(
                    RASA_URL,
                    json={"sender": "utilisateur", "message": question},
                    timeout=5  # sécurité pour éviter blocage
                )
                data = response.json()
                reponse = " ".join([d["text"] for d in data if "text" in d])
            except Exception as e:
                reponse = f"Erreur de communication avec le bot Rasa : {e}"

            # Stockage question + réponse en BDD
            nouvelle_question = Question(question=question, reponse=reponse)
            db.session.add(nouvelle_question)
            db.session.commit()

        return render_template("reponse.html", question=question, reponse=reponse)

    return render_template("reponse.html", question=None, reponse=None, message_accueil=message_accueil)

# Route pour enregistrer une remarque
@app.route("/remarque", methods=["POST"])
def remarque():
    texte_remarque = request.form.get("remarque")
    if texte_remarque and texte_remarque.strip() != "":
        nouvelle_remarque = Remarque(texte=texte_remarque.strip())
        db.session.add(nouvelle_remarque)
        db.session.commit()
        flash("Merci pour votre remarque !", "success")
    else:
        flash("La remarque ne peut pas être vide.", "error")
    return redirect(url_for("formulaire"))

# Lancer l'app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
