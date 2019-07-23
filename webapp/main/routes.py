from flask import Blueprint, render_template, request, url_for, flash, redirect, request, abort
from webapp.main.forms import SchoolForm, ClassForm
import optimizers.optimizer as optimizer

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def default():
    return redirect(url_for('main.home'))

@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SchoolForm()
    if form.validate_on_submit():
        print(form.name.data)
        return redirect(url_for('main.search', university=form.name.data, semester=form.semester.data))
    return render_template("home.html", form=form)

@main.route("/<string:university>", methods=['GET', 'POST'])
def search(university):
    classes = request.args.get("classes", type=str)
    semester = request.args.get("semester", type=str)
    if university in ['queens'] and semester in ['F', 'W', 'S']:
        form = ClassForm()
        if form.validate_on_submit():
            classes=form.classes.data
            if classes:
                return redirect(url_for('main.search', university=university, semester=semester, classes=form.classes.data))
        if classes:
            ledger, class_list = optimizer.parse_string(classes, semester, university)
            return render_template("search.html", university=university, form=form, class_list=class_list, ledger=ledger, len=len(class_list))
        return render_template("search.html", university=university, form=form)
    else:
        abort(404)

@main.route("/about")
def about():
    return render_template("about.html")
