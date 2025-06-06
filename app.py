import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Configuration manuelle de la base PostgreSQL sur Render
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bdd_entrainement_rasa_user:X4dXXHlehramSkQvDYWAyGoSz9VcnaFW@dpg-d109t40gjchc73agl4c0-a.oregon-postgres.render.com/bdd_entrainement_rasa"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Définition du modèle Question
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)

# ✅ Création de la table si elle n'existe pas encore
with app.app_context():
    db.create_all()

# ✅ Route principale
@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        contenu_question = request.form.get("question")
        if contenu_question:
            nouvelle_question = Question(question=contenu_question)
            db.session.add(nouvelle_question)
            db.session.commit()
            return render_template("thank_you.html")
    return render_template("form.html")

# ✅ Lancement de l'application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
