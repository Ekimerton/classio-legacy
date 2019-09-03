from flask import Blueprint, render_template, request, url_for, flash, redirect, request, abort
from webapp.main.forms import SchoolForm, ClassForm
import webapp.main.utils as utils
import optimizers.optimizer as optimizer
import datetime

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def default():
    return redirect(url_for('main.home'))


@main.route("/home", methods=['GET', 'POST'])
def home():
    form = SchoolForm()
    if form.validate_on_submit():
        return redirect(url_for('main.search', university=form.name.data))
    return render_template("home.html", form=form)


def pretty_time(timestamp):
    if len(timestamp) == 10:
        return timestamp[:2] + " " + timestamp[2:4] + ":" + timestamp[4:6] + "-" + timestamp[6:8] + ":" + timestamp[8:]
    elif len(timestamp) == 8:
        return timestamp[:2] + ":" + timestamp[2:4] + "-" + timestamp[4:6] + ":" + timestamp[6:8]


@main.route("/<string:university>", methods=['GET', 'POST'])
def search(university):
    uni_dict = {'queens': "Queen's University",
                'waterloo': 'University of Waterloo',
                'ubc': 'University of British Columbia'}
    day_dict = {1: 'Monday', 2: 'Tuesday',
                3: 'Wednesday', 4: 'Thursday', 5: 'Friday'}
    classes = request.args.get("classes", type=str)
    semester = request.args.get("semester", type=str)
    lunch = request.args.get("l", type=int)
    dinner = request.args.get('d', type=int)
    offtime = request.args.get('o', type=int)
    lunch_time = request.args.get("lunch", type=str)
    dinner_time = request.args.get("dinner", type=str)
    if university in ['queens', 'waterloo', 'ubc']:
        form = ClassForm()
        if form.validate_on_submit():
            lunch_time = utils.pad_hour(form.lunch_start.data.hour) + utils.pad_hour(form.lunch_start.data.minute) + \
                utils.pad_hour(form.lunch_end.data.hour) + \
                utils.pad_hour(form.lunch_end.data.minute)
            dinner_time = utils.pad_hour(form.dinner_start.data.hour) + utils.pad_hour(form.dinner_start.data.minute) + \
                utils.pad_hour(form.dinner_end.data.hour) + \
                utils.pad_hour(form.dinner_end.data.minute)
            classes = form.classes.data
            if classes:
                return redirect(url_for('main.search', university=university, semester=form.semester.data, classes=classes, l=form.lunch.data, d=form.dinner.data, o=form.offtime.data, lunch=lunch_time, dinner=dinner_time))
        if classes:
            form.lunch_start.data = datetime.time(11, 30)
            form.lunch_end.data = datetime.time(13, 30)
            form.dinner_start.data = datetime.time(18, 30)
            form.dinner_end.data = datetime.time(20, 30)
            score_params = {'lunch': lunch/100, 'dinner': dinner/100,
                            'offtime': offtime/100, 'lunch_time': lunch_time, 'dinner_time': dinner_time}
            clean_classes = classes.replace(" ", "")
            clean_classes = clean_classes.upper()
            ledger, class_list = optimizer.parse_string(
                clean_classes, semester, university, score_params)
            num_of_entries = len(class_list)
            class_list = class_list[:100]
            days_list = optimizer.parse_timetables(class_list)
            return render_template("search.html", university=uni_dict[university], semester=semester, form=form, class_list=class_list, ledger=ledger, len=num_of_entries, pretty_time=pretty_time, round=round, days_list=days_list, day_dict=day_dict)
        form.lunch_start.data = datetime.time(11, 30)
        form.lunch_end.data = datetime.time(13, 30)
        form.dinner_start.data = datetime.time(18, 30)
        form.dinner_end.data = datetime.time(20, 30)
        return render_template("search.html", university=uni_dict[university], form=form)
    else:
        abort(404)


@main.route("/about")
def about():
    return render_template("about.html")
