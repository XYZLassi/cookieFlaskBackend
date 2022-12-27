import click
from flask import Blueprint

from {{cookiecutter.package_name}}.ext import db

bp_cli = Blueprint("user", __name__)


def create_user(name: str, email: str, password: str, is_admin: bool = False):
    from {{cookiecutter.package_name}}.models.user import User
    user = User(username=name,email=email)
    user.set_password(password)
    user.is_admin = is_admin

    db.session.add(user)
    db.session.commit()


@bp_cli.cli.command('create')
@click.argument('fn')
@click.argument('email')
@click.argument('password')
def cli_create_user(name: str, email: str, password: str):
    create_user(name, email, password)


@bp_cli.cli.command('create_admin')
@click.argument('fn')
@click.argument('email')
@click.argument('password')
def cli_create_admin(name: str, email: str, password: str):
    create_user(name, email, password, is_admin=True)
