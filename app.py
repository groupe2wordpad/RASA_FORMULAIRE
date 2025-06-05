import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Récupération de l'URL de la base de données externe Render
database_url = os.environ.get('DATABASE_URL')

# Correction obligatoire pour SQLAlchemy : "postgres://" => "postgresql://"
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    question = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        contenu_question = request.form.get("question")

        nouvelle_question = Question(nom=nom, email=email, question=contenu_question)
        db.session.add(nouvelle_question)
        db.session.commit()

        return render_template("thank_you.html")

    return render_template("form.html")

@app.route("/questions", methods=["GET"])
def afficher_questions():
    questions = Question.query.order_by(Question.id.desc()).all()
    return render_template("questions.html", questions=questions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
