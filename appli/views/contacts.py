from flask import render_template

from appli.app import app


@app.route('/contacts/')
def contacts():
    return render_template('contacts.html', title="Contacts")
