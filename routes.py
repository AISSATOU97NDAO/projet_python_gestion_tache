from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from models import *


user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@user_bp.route('/')
def login():
    return render_template("login.html")

@user_bp.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
#    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Veuillez vérifier vos informations de connexion et réessayer.')
        return redirect(url_for('user.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('tache.index'))

@user_bp.route('/signup')
def signup():
    return render_template("signup.html")

@user_bp.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in db

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('l adresse mail existe déjà')
        return redirect(url_for('user.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    new_user.create()

    return redirect(url_for('user.login'))

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

tache_bp = Blueprint('tache', __name__)

#This is the index route where we are going to
#query on all our employee data
@tache_bp.route('/index')
@login_required
def index():
    taches = Tache.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", user=current_user, taches=taches)

#this route is for inserting data to postgres database via html forms
@tache_bp.route('/insert', methods = ['POST'])
@login_required
def insert():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        date_echeance = request.form['date_echeance']
        user_id = current_user.id
        nouvelle_tache = Tache(titre, description, date_echeance, user_id)
        nouvelle_tache.create()
        flash("Vous avez créé une tache avec succés")
        return redirect(url_for('tache.index'))

#this is our update route where we are going to update our task
@tache_bp.route('/update', methods = ['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        tache_modifie = Tache.query.get(request.form.get('id'))
        tache_modifie.update(request.form)
        flash("Tache modifiée avec succes")
        return redirect(url_for('tache.index'))

#This route is for deleting our employee
@tache_bp.route('/delete/<id>/', methods = ['GET', 'POST'])
@login_required
def delete(id):
    tache_a_supprime = Tache.query.get(id)
    tache_a_supprime.delete()
    flash("Tache supprimée")
    return redirect(url_for('tache.index'))