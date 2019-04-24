from . import web
from flask import render_template



@web.route('/about/')
def about():
    return render_template('about.html')