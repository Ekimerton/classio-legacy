from flask import Blueprint, render_template, request, url_for, flash, redirect, request, abort
from webapp.main.forms import SchoolForm, ClassForm
import optimizers.optimizer as optimizer

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def default():
    return redirect(url_for('main.search', university="queens"))

@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SchoolForm()
    if form.validate_on_submit():
        print(form.name.data)
        return redirect(url_for('main.search', university=form.name.data))
    return render_template("home.html", form=form)

def pretty_time(timestamp):
    return timestamp[:2] + " " + timestamp[2:4] + ":" + timestamp[4:6] + "-" + timestamp[6:8] + ":" + timestamp[8:]

@main.route("/<string:university>", methods=['GET', 'POST'])
def search(university):
    uni_dict = {'queens':"Queen's University"}
    classes = request.args.get("classes", type=str)
    semester = request.args.get("semester", type=str)
    if university in ['queens']:
        form = ClassForm()
        if form.validate_on_submit():
            classes=form.classes.data
            if classes:
                return redirect(url_for('main.search', university=university, semester=form.semester.data, classes=form.classes.data))
        if classes:
            clean_classes = classes.replace(" ", "")
            clean_classes = clean_classes.upper()
            ledger, class_list = optimizer.parse_string(clean_classes, semester, university)
            return render_template("search.html", university=uni_dict[university], semester=semester, form=form, class_list=class_list, ledger=ledger, len=len(class_list), pretty_time=pretty_time)
        return render_template("search.html", university=uni_dict[university], form=form)
    else:
        abort(404)

@main.route("/about")
def about():
    return render_template("about.html")
