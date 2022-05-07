#!/usr/bin/env bash
# Comment
poetry run flask db upgrade
poetry run flask run --host=0.0.0.0 --port=$FLASK_PORT
