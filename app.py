from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Création du dossier "data" s'il n'existe pas
if not os.path.exists("data"):
    os.makedirs("data")

@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        question = request.form.get("question")

        # Sauvegarde dans un fichier texte
        with open("data/questions.txt", "a", encoding="utf-8") as f:
            f.write(f"Nom : {nom}\nEmail : {email}\nQuestion : {question}\n---\n")

        # Affiche la page de remerciement
        return render_template("thank_you.html")
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
