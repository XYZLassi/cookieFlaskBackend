#!/usr/bin/env bash

export FLASK_APP="src/wsgi.py"

flask db migrate
flask db upgrade
