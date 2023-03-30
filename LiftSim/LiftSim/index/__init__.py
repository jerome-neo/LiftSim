from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .forms import addRequestForm
# from ..simulation import Main

index = Blueprint('index', __name__, template_folder='templates')


def getNewRequest():
    form = addRequestForm()
    num_of_pax = request.form.get('num_of_pax')
    src = request.form.get('src')
    dest = request.form.get('dest')
    return [num_of_pax, src, dest]


@index.route('/', methods=['GET', 'POST'])
def show_index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        new_req = getNewRequest()
        """ call model, change params"""
        plan, avg_waiting_time = Main.run(new_req)
        """"""
        return render_template('index.html', plan=plan, avg_waiting_time=avg_waiting_time)
