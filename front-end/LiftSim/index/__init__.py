from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)


simulation = Blueprint('simulation', __name__, template_folder='templates')
summary = Blueprint('summary', __name__, template_folder='templates')


@simulation.route('/simulation')
def page1():
    return render_template('simulation.html')


@summary.route('/summary')
def page2():
    return render_template('summary.html')
