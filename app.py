import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration base de données
database_url = os.environ.get('DATABASE_URL')

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

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



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
