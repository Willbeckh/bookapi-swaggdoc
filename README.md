# bookapi-swaggdoc
swagger documentation for a flask API

## Setup
1. Clone repo
2. create and change into directory
3. Set Flask environment (ps: check the `config.py` file)
  - `FLASK_ENV=default` uses sqlite
  - `FLASK_ENV=postgres` uses postgres db

4. set virtualenv with `pipenv --three`
5. Install with `pipenv install`

## Running
- type: `python run.py` serving point of the API
- app running on `http://127.0.0.1:5000/`
- Documentation being served on `/api-docs` endpoint

