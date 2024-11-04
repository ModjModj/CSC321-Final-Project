from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

#Calls home html for home page
@views.route("/")
def home():
    return render_template("home.html")

#Calls archive html for archive page
@views.route("/archive")
#Forces user to login to view the page
@login_required
def archive():
    return render_template("archive.html")