from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Création du dossier "data" s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

# Configuration base de données SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db = SQLAlchemy(app)

# Définition du modèle Question
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.Text, nullable=False)

# Création automatique de la base et de la table
with app.app_context():
    db.create_all()

# Route principale : formulaire
@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        contenu_question = request.form.get("question")

        # Enregistrement dans la base
        nouvelle_question = Question(nom=nom, email=email, question=contenu_question)
        db.session.add(nouvelle_question)
        db.session.commit()

        return render_template("thank_you.html")

    return render_template("form.html")

# Lancement de l'app Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
