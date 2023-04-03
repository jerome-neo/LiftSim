from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .forms import addRequestForm

# from ..simulation import Main

index = Blueprint('index', __name__, template_folder='templates')


def getNewRequest():
    form = addRequestForm()
    time = request.form.get('num_of_pax')
    src = request.form.get('src')
    dest = request.form.get('dest')
    return [num_of_pax, src, dest]


@index.route('/liftsim')
def page1():
    return render_template('index.html')


@index.route('/summary')
def page2():
    return render_template('summary.html')
