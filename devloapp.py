from flask import render_template, Flask, session, redirect, url_for, g
from App import home, inscription, verification, connexion, resend, onthefly, forgot_password
from App.utils.bdd import DevloBDD
from App.utils.utils import is_connected
from werkzeug.middleware.proxy_fix import ProxyFix
from App.admin_space import admin_space
from os import path, getcwd, environ
from json import load
from dotenv import load_dotenv

env = os.path.join(os.getcwd(), '.env')
if os.path.exists(env):
    load_dotenv(env)


app = Flask(__name__)
app.secret_key = "banane"
app.which = "devlobdd"
app.config["UPLOAD_FOLDER"] = "tmp/"
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=0, x_host=1, x_prefix=1
)

if environ.keys().__contains__("SERVER_NAME") and environ["ENV"] == "prod":
    app.config["SERVER_NAME"] = environ["SERVER_NAME"]
else:
    app.config["SERVER_NAME"] = "127.0.0.1:5555"


file_path = path.abspath(path.join(getcwd(), "config.json"))  # Trouver le chemin complet du fichier config.json

# Lecture du fichier JSON
with open(file_path, 'r') as file:
    config_data = load(file)  # Ouverture du fichier config.json

db = DevloBDD(config_data['database']['username'], config_data['database']['password'], config_data['database']['addr'], config_data['database']['port'])

db.create_bdd()

@app.route("/", subdomain="<subdomain>")
def index(subdomain):
    print(f"Acces depuis {subdomain} !")
    if subdomain != "devlowave":
        return onthefly.gen_on_the_fly(subdomain, db)
    return render_template("index.html")

@app.route("/")
def accueil():
    return render_template("index.html")



"""
ESPACE INSCRIPTION/CONNEXION
"""


@app.route("/inscription", methods=("GET", "POST"))
def route_inscription():
    return inscription.inscription(db)


@app.route("/verification", methods=("GET", "POST"))
def route_verification():
    return verification.verify_email(db)


@app.route("/connexion", methods=("GET", "POST"))
def route_connexion():
    return connexion.connexion(db)


@app.route("/forgotpassword", methods=("GET", "POST"))
def route_forgot():
    return forgot_password.forgot_password(db)


@app.route("/reset_password", methods=("GET", "POST"))
def route_reset():
    return forgot_password.reset_password(db)


@app.route("/resend", methods=("GET", "POST"))
def route_resend():
    return resend.resend_email(db)


"""
ESPACE MODIFICATION DU SITE
"""


@app.route("/home")
def route_home():
    if is_connected(session, db):
        return home.index(db)
    return redirect(url_for('route_connexion'))


@app.route("/home/account")
def route_account():
    if is_connected(session, db):
        return home.account()
    return redirect(url_for('route_connexion'))


@app.route("/home/editeur", methods=("GET", "POST"))
def route_editeur():
    # C'est le DASHBOARD Éditeur
    if is_connected(session, db):
        return render_template("home/editeur.html")
    return redirect(url_for('route_connexion'))

@app.route("/home/preview", methods=("GET", "POST"))
def route_preview():
    # C'est le DASHBOARD Éditeur
    if is_connected(session, get_db()):
        return home.preview()
    return redirect(url_for('route_connexion'))





@app.route("/editeur/beta/editeur", methods=("GET", "POST"))
def route_beta():
    if is_connected(session, db):
        return home.editeur()
    return redirect(url_for('route_connexion'))

@app.route("/home/hebergement", methods=("GET", "POST"))
def route_hebergement():
    if is_connected(session, db):
        return home.hebergement(db)
    return redirect(url_for('route_connexion'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('accueil'))


"""
ESPACE ERREURS
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error/500.html', error=e), 500

"""
ESPACE ADMIN
"""
@app.route("/admin_space", methods=("GET", "POST"))
def route_admin_space():
    return admin_space.load_panel(db)

@app.route("/admin_space/website_validator", methods=("GET", "POST"))
def route_admin_space_website_validator():
    return admin_space.load_website_validator(db)


if __name__ == "__main__":
    # therms-and-conditions
    app.run(host="127.0.0.1", port=5555, debug=True)
