from flask import Flask, render_template
from cookbook.routes import cookbook_bp
from journal.database import init_journal_db
from journal.routes import journal_bp
from car.routes import car_bp
from scavenger_hunt.routes import scavenger_hunt_bp
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
port = int(os.environ.get('PORT', 4000))

init_journal_db(app)

app.register_blueprint(cookbook_bp)
app.register_blueprint(journal_bp)
app.register_blueprint(car_bp)
app.register_blueprint(scavenger_hunt_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=port)
