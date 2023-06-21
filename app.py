from flask import Flask
from flask_login import LoginManager   #c'est pour gérer la gestion de l'autentification et la session utilisateur
from models import db, User
from routes import *                  # c'est pour definir les routes de notre page

app = Flask(__name__)
app.secret_key = "Secret Key"          # c'est pour securiser les sessions utilisations et les cookies
#Configuration de la base de données SqlAlchemy avec Postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flask:flask@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # c'est pour intialiser une extension

with app.app_context():
    db.create_all()

app.register_blueprint(user_bp)
app.register_blueprint(tache_bp)

login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)