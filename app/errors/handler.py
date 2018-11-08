from flask import Flask, render_template
from . import errors

@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

@errors.app_errorhandler(400)
def handle_bad_request(error):
    return render_template('errors/400.html'), 400
