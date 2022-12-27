#!/usr/bin/env bash

export FLASK_APP="src/wsgi.py"

rm -r migrations
rm app.db

flask db init
flask db migrate
flask db upgrade

flask user create_admin TestUser "{{cookiecutter.admin_email}}" "test"
