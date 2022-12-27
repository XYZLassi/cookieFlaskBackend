#!/usr/bin/env bash

export FLASK_APP="src/wsgi.py"
export PYTHONPATH="${PYTHONPATH}:$PWD/$(basename src)"
export TESTING=1

pytest --cov-report html --cov=src ./test
