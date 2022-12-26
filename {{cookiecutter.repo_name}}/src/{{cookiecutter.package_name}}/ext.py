__all__ = ['db', 'migrate', 'socket', 'login', 'scheduler']

from apscheduler.schedulers.blocking import BlockingScheduler
from engineio.payload import Payload
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from pytz import utc
from sqlalchemy import MetaData

Payload.max_decode_packets = 100

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
socket = SocketIO()
login = LoginManager()

scheduler = BlockingScheduler(timezone=utc)
