from flask import Flask,render_template,redirect,request,url_for,session
import sqlite3

app=Flask(__name__)

app.secret_key="ma_clé_secrète"

@app.route("/")
def acceuil():

    if "utilisateur_id" not in session:
        return redirect(url_for("connexion"))
    name=session["name"]
    return render_template("acceuil.html",name=name)

# BASE DE DONNEES

def init_db():
    conn=sqlite3.connect("miniconnect.bd")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conctacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilisateur_id INTEGER NOT NULL,
        conctact_id INTEGER NOT NULL
    )
 """)

    conn.commit()
    conn.close()

# INSCRIPTION

@app.route("/inscription",methods=["GET","POST"])
def inscription():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email").strip().lower()
        password=request.form.get("mot_de_passe")
        confirmation=request.form.get("confirmation")

        if password!=confirmation:
            return render_template("inscription.html",erreur="Les mots de passent ne correspondent")

        conn=sqlite3.connect("miniconnect.bd")
        try:
            conn.execute("""
                INSERT INTO utilisateurs(name,email,password)
                VALUES (?,?,?)
            """,(name,email,password))

            conn.commit()

            utilisateur=conn.execute("""
            SELECT id,name FROM utilisateurs
            WHERE email=?
            """,(email,)).fetchone()

            conn.close()

            session["utilisateur_id"]=utilisateur[0]
            session["name"]=utilisateur[1]

        except sqlite3.IntegrityError:
            return render_template("inscription.html",erreur="Cet email existe deja !")

        print("name =", name)
        print("email =", email)
        print("password =", password)
        print("confirmation =", confirmation)

        return redirect(url_for("acceuil"))
    
    return render_template("inscription.html")


# CONNEXION

@app.route("/connexion",methods=["GET","POST"])
def connexion():

    if request.method == "POST":
        password=request.form.get("mot_de_passe")
        email=request.form.get("email").strip().lower()

        conn=sqlite3.connect("miniconnect.bd")
        utilisateur=conn.execute("""
        SELECT id,name,password FROM utilisateurs
        WHERE email=?
        """,(email,)).fetchone()

        conn.close

        if utilisateur is None:
            return render_template("connexion.html",erreur="Mot de passe ou email incorrect")
        elif password != utilisateur[2]:
            return render_template("connexion.html",erreur="Mot de passe ou email incorrect")
        else:
            session["utilisateur_id"]=utilisateur[0]
            session["name"]=utilisateur[1]
            return redirect(url_for("acceuil"))

    return render_template("connexion.html")

# DECONNEXION
@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect(url_for("connexion"))

# PROFIL
@app.route("/profil")
def profil():

    if "utilisateur_id" not in session:
        return redirect(url_for('connexion'))

    utilisateur_id=session["utilisateur_id"]

    conn=sqlite3.connect("miniconnect.bd")
    utilisateur=conn.execute("""
    SELECT id,name,email FROM utilisateurs
    WHERE id=?
    """,(utilisateur_id,)).fetchone()

    return render_template ("profil.html",
    utilisateur=utilisateur)

@app.route("/conctacts",methods=["GET","POST"])
def conctacts():

    if "utilisateur_id" not in session:
            return redirect(url_for('connexion'))
    
    utilisateur_id=session["utilisateur_id"]

    conn=sqlite3.connect("miniconnect.bd")

    erreur=""        
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")

        test=conn.execute("""
                        SELECT id FROM utilisateurs
                        WHERE email=?
                        """,(email,)).fetchone()
        
        try:
            if test:
                if test[0]==utilisateur_id:
                    erreur="Vous ne pouvez pas vous ajoutez vous-meme"
                conn.execute("""
                INSERT INTO conctacts (utilisateurs_id,conctacts_id)
                VALUES (?,?)
                """,(utilisateur_id,test[0]))

                conn.commit()
            else:
                erreur="Ce compte n'existe pas"
        except sqlite3.IntegrityError:
            erreur="Cet email existe deja ! Ajout impossible"
            

    contacts=conn.execute("""
            SELECT utilisateurs.id,utilisateurs.name,utilisateurs.email
            FROM conctacts
            JOIN utilisateurs
            ON conctacts.conctacts_id=utilisateurs.id
            WHERE conctacts.utilisateurs_id=?
            """,(utilisateur_id,)).fetchall()
        
    conn.close()

    return render_template('conctacts.html',contacts=contacts,erreur=erreur)

@app.route("/supprimer_conctact,<int:conctact_id>")
def supprimer_conctact(conctact_id):

    if "utilisateur_id" not in session:
        return redirect(url_for('connexion'))

    utilisateur_id=session['utilisateur_id']

    conn=sqlite3.connect('miniconnect.bd')
    conn.execute("""
    DELETE FROM conctacts
    WHERE utilisateurs_id=?
    AND conctacts_id=?
    """,(utilisateur_id,conctact_id))

    conn.commit()
    conn.close()

    return redirect(url_for('conctacts'))
    
@app.route("/message")
def message():
    return render_template("message.hmtl")

    







"""
@app.route("/recherche")
def recherche():

    mot = request.args.get("recherche")

    return render_template(
        "recherche.html",
        mot=mot
    )

"""

# Lancer l'application python
if __name__=="__main__":
    init_db()
    app.run(debug=True)