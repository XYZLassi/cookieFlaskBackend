import datetime

import flask
from dateutil import tz

bp = flask.Blueprint('filter', __name__, template_folder='templates')


@bp.add_app_template_filter
def df(date, fmt=None):
    from_zone = tz.gettz('UTC')
    to_zone = tz.tzlocal()

    if isinstance(date, datetime.datetime):
        date = date.replace(tzinfo=from_zone).astimezone(to_zone)

        return date.strftime(fmt or '%d.%m.%y %H:%M:%S')
    elif isinstance(date, datetime.date):
        return date.strftime(fmt or '%d.%m.%y')


@bp.add_app_template_filter
def percent(value, decimal=','):
    if value is None:
        return '- %'
    value *= 100

    return f'{value:.2f} %'.replace('.', decimal)
