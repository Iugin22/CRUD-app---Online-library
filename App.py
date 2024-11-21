from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "cheie"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@127.0.0.1/biblioteca"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Carti(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titlu = db.Column(db.String(50), nullable=False)
    autor = db.Column(db.String(50), nullable=False)
    gen = db.Column(db.String(50), nullable=False)
    editura = db.Column(db.String(50), nullable=False)
    anpublicare = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(50), nullable=False)

    def __init__(self, titlu, autor, gen, editura, anpublicare, rating):
        self.titlu = titlu
        self.autor = autor
        self.gen = gen
        self.editura = editura
        self.anpublicare = anpublicare
        self.rating = rating


@app.route("/")
def index():
    datele_cartii = db.session.query(Carti)
    return render_template("index.html", data=datele_cartii)


@app.route("/adaugare", methods=["GET", "POST"])
def adaugare_date():
    if request.method == "POST":
        titlu = request.form["titlu"]
        autor = request.form["autor"]
        gen = request.form["gen"]
        editura = request.form["editura"]
        anpublicare = request.form["anpublicare"]
        rating = request.form["rating"]

        adauga = Carti(titlu, autor, gen, editura, anpublicare, rating)
        db.session.add(adauga)
        db.session.commit()

        return redirect(url_for("index"))
    return render_template("adaugare.html")

@app.route("/editare/<int:id>")
def editare_date(id):
    datele_cartii = Carti.query.get(id)
    return render_template('editare.html', data = datele_cartii)

@app.route("/aplica_editarile", methods = ["POST", "GET"])
def aplica_editarile():
    datele_cartii = Carti.query.get(request.form.get("id"))

    datele_cartii.titlu = request.form["titlu"]
    datele_cartii.autor = request.form["autor"]
    datele_cartii.gen = request.form["gen"]
    datele_cartii.editura = request.form["editura"]
    datele_cartii.anpublicare = request.form["anpublicare"]
    datele_cartii.rating = request.form["rating"]

    db.session.commit()
    return redirect(url_for("index"))

@app.route("/sterge_carte/<int:id>")
def sterge_carte(id):
    datele_cartii = Carti.query.get(id)
    db.session.delete(datele_cartii)
    db.session.commit()

    return redirect(url_for("index"))

app.run(debug=True)