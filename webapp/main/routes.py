from flask import Blueprint, render_template, request, url_for, flash, redirect, request, abort
from webapp.main.forms import SchoolForm

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    form = SchoolForm()
    return render_template("home.html", form=form)

@main.route("/about")
def about():
    return render_template("about.html")
