from __future__ import annotations

__all__ = ['User']

from typing import Optional, Iterator

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from {{cookiecutter.package_name}}.ext import db, login
from {{cookiecutter.package_name}}.tools.db import ModelMixin


class User(db.Model, UserMixin, ModelMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.BOOLEAN, server_default="0", default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    @classmethod
    def current_user(cls: User) -> Optional[User]:
        from flask_login import current_user
        if current_user.is_authenticated:
            return current_user
        return None

    @classmethod
    def get_by_username(cls: User, name: str) -> Optional[User]:
        return cls.first(username=name)

    def all_active_task(self, field=None) -> Iterator:
        from .task import Task
        return Task.all_active_task(self.id, field=field)

    def launch_task(self, fn, *args,
                    description: str = None, field: str = None,
                    **kwargs):
        from .task import Task
        return Task.launch_task(fn, self.id, *args,
                                description=description, field=field, **kwargs)

    def __repr__(self):
        return "<User {}>".format(self.username)


@login.user_loader
def load_user(id) -> User:
    return User.get(id)
