from flask import Blueprint, redirect, render_template, url_for, request, flash
from __init__ import db
from tables import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

#Sets up login functionality
@auth.route("/login", methods = ['GET', 'POST'])
def login():
    #If the submit button is pressed
    if(request.method == 'POST'):
        #Retrieve values input in the email and password sections
        email = request.form.get("email")
        password = request.form.get("password")
        
        #Search for given email in database
        user = User.query.filter_by(email=email).first()
        #If the user exists, verify their password
        if(user):
            #If the given password when hashed is the same as the stored password, login
            if(check_password_hash(user.password, password)):
                flash('Successfully Logged In! Happy Posting!', category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            #If the hashed password is incorrect, return an error
            else:
                flash('Incorrect Passoword', category='error')
        #If the given email doesn't exist, return an error
        else:
            flash('Email given is not associated with an existing account', category='error')
    return render_template("login.html")

@auth.route("/sign-up", methods = ['GET', 'POST'])
def sign_up():
    #If the submit button is pressed
    if(request.method == 'POST'):
        #Retrieve all inputted values
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #Check if the given username or password already exist
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        #Return an error if the given email exists
        if email_exists:
            flash('Email is already in use.', category='error')
        #Return an error if the given username exists
        elif username_exists:
            flash('Username is already in use.', category='error')
        #Return an error if the passwords don't match
        elif (password1 != password2):
            flash('Password don\'t match!', category='error')
        #Return an error if the given username is too short
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        #Return an error if the given password is too short
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        #Return an error if the given email is too short
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        #Login if all tests are passed
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html")

#Logout and redirect to home
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))