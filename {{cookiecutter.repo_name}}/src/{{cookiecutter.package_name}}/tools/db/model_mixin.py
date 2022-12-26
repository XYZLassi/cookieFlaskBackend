__all__ = ['ModelMixin', 'inject_session']

import base64
import os
from typing import TypeVar, Type, Iterator, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import abort
from sqlalchemy.orm import Query

T = TypeVar('T')


def inject_session(func):
    def wrapper(*args, **kwargs):
        from {{cookiecutter.package_name}}.ext import db

        if 'session' in kwargs:
            return func(*args, **kwargs)
        with db.create_session({})() as tmp_session:
            return func(*args, session=tmp_session, **kwargs)

    return wrapper


class ModelMixin:
    @staticmethod
    def get_current_user_id(context) -> Optional[int]:
        from {{cookiecutter.package_name}}.models.user import User
        current_user = User.current_user()
        return current_user.id if current_user else None

    @classmethod
    def q(cls: Type[T], **kwargs) -> Query:
        q: Query = cls.query
        return q

    @classmethod
    def all(cls: Type[T], **kwargs) -> Iterator[T]:
        q: Query = cls.query
        for item in q.filter_by(**kwargs):
            yield item

    @classmethod
    def get(cls: Type[T], doc_id) -> Optional[T]:
        q: Query = cls.query
        item: Optional[T] = q.get(doc_id)
        return item

    @classmethod
    def get_or_404(cls: Type[T], doc_id) -> T:
        item = cls.get(doc_id)

        if not item:
            abort(404)

        return item

    @classmethod
    def first(cls: Type[T], **kwargs) -> Optional[T]:
        q: Query = cls.query
        item: Optional[T] = q.filter_by(**kwargs).first()
        return item

    @staticmethod
    def encrypt_credentials(credentials_string: str) -> str:
        from flask import current_app
        key: str = current_app.config['SECRET_KEY']
        password = key.encode('UTF-8')
        salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,

        )

        key_b64 = base64.urlsafe_b64encode(kdf.derive(password))
        crypt_obj = Fernet(key_b64)

        base64_salt = base64.urlsafe_b64encode(salt).decode('UTF-8')
        base64_credentials = base64.urlsafe_b64encode(crypt_obj.encrypt(credentials_string.encode('UTF-8'))) \
            .decode('UTF-8')

        return f'{base64_salt}:{base64_credentials}'

    @staticmethod
    def decrypt_credentials(secure_string: str) -> str:
        from flask import current_app

        base64_salt, base64_token = secure_string.split(':', maxsplit=2)
        salt = base64.urlsafe_b64decode(base64_salt)
        token = base64.urlsafe_b64decode(base64_token)

        key: str = current_app.config['SECRET_KEY']
        password = key.encode('UTF-8')

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )

        key_b64 = base64.urlsafe_b64encode(kdf.derive(password))
        crypt_obj = Fernet(key_b64)

        credentials_string = crypt_obj.decrypt(token).decode('UTF-8')

        return credentials_string
