from flask import render_template, Flask
from App import inscription, verification

app = Flask(__name__)
app.debug = True
app.secret_key = "banane" 


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/inscription", methods=("GET", "POST"))
def route_inscription():
    print("Je me situe ici")
    return inscription.inscription()

@app.route("/verification", methods=("GET", "POST"))
def route_verification():
    return verification.verify_email()

if __name__ == "__main__":
    app.run(port=5555)