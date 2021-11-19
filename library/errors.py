from flask import jsonify
from library.main import app

@app.errorhandler(404)
def not_found_err(error):
    return jsonify({"message": "Page not found!"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "oops! Internal server error"}), 500