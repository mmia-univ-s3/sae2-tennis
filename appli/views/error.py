from flask import render_template

from appli.app import app


@app.errorhandler(404)
def e404(_):
    return render_template('error.html', error_code=404, error_message="La page est introuvable.")


@app.errorhandler(500)
def e500(_):
    return render_template('error.html', error_code=500, error_message="Une erreur s'est produite.")


@app.errorhandler(405)
def e405(_):
    return render_template('error.html', error_code=405,
                           error_message="Cette méthode n'est pas autorisée.")
