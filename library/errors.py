from flask import jsonify
from library.main import app

@app.errorhandler(404)
def not_found_err(error):
    return jsonify({"message": "resource not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "oops server error"}), 500