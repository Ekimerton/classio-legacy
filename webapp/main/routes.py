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
        return redirect(url_for('main.search', university=form.name.data))
    return render_template("home.html", form=form)

def pretty_time(timestamp):
    return timestamp[:2] + " " + timestamp[2:4] + ":" + timestamp[4:6] + "-" + timestamp[6:8] + ":" + timestamp[8:]

@main.route("/<string:university>", methods=['GET', 'POST'])
def search(university):
    uni_dict = {'queens':"Queen's University", 'waterloo':'University of Waterloo'}
    classes = request.args.get("classes", type=str)
    semester = request.args.get("semester", type=str)
    page = request.args.get("page", type=int)
    lunch = request.args.get("l", type=int)
    dinner = request.args.get('d', type=int)
    offtime = request.args.get('o', type=int)
    if university in ['queens', 'waterloo']:
        form = ClassForm()
        form.lunch_time.data = "11:30-13:30"
        form.dinner_time.data = "18:30-20:30"
        if form.validate_on_submit():
            classes=form.classes.data
            if classes:
                return redirect(url_for('main.search', university=university, semester=form.semester.data, classes=classes, l=form.lunch.data, d=form.dinner.data, o=form.offtime.data))
        if classes:
            score_params = {'lunch':lunch/100, 'dinner':dinner/100,'offtime':offtime/100}
            clean_classes = classes.replace(" ", "")
            clean_classes = clean_classes.upper()
            ledger, class_list = optimizer.parse_string(clean_classes, semester, university, score_params)
            return render_template("search.html", university=uni_dict[university], semester=semester, form=form, class_list=class_list[:100], ledger=ledger, len=len(class_list), pretty_time=pretty_time, round=round)
        return render_template("search.html", university=uni_dict[university], form=form)
    else:
        abort(404)

@main.route("/about")
def about():
    return render_template("about.html")
