import os
from flask import Flask, config
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import app_config
from flask_swagger_ui import get_swaggerui_blueprint


config_name = os.getenv('FLASK_ENV', 'default')

app = Flask(__name__)
# app.config.from_object(Config)
app.config.from_object(app_config[config_name])


# swagger ui configs
SWAGGER_URL = '/api-docs'
API_URL = '/static/swagger.yml'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app-name': 'book manager'
    }
)

# register blueprint
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

# db object
db = SQLAlchemy(app)

# create db tables
@app.before_first_request
def create_tables():
    db.create_all()

migrate = Migrate(app, db, render_as_batch=True) # obj for db migrations
CORS(app)

# from library import models, resources
import library.resources as resources
import library.errors as errors
