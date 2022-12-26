from __future__ import annotations

__all__ = ['Task']

import functools
from typing import Optional, Iterator, Callable

from rq.job import Job

from {{cookiecutter.package_name}}.ext import db
from {{cookiecutter.package_name}}.tools.db import ModelMixin


class Task(db.Model, ModelMixin):
    __tablename__ = 'tasks'

    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text, index=True)
    description = db.Column(db.Text)

    field = db.Column(db.String, nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    owner = db.relationship('User')

    @functools.cached_property
    def rq_job(self) -> Optional[Job]:
        import rq
        import redis

        from flask import current_app

        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    @property
    def progress(self) -> int:
        return self.rq_job.meta.get('progress', 0) if self.rq_job is not None else 100

    @classmethod
    def all_active_task(cls, user_id: int = None, field: str = None) -> Iterator[Task]:
        query = cls.query

        if user_id:
            query = query.filter_by(owner_id=user_id)
        if field:
            query = query.filter_by(field=field)

        for item in query:
            job: Job = item.rq_job
            if job and (job.is_queued or job.is_started):
                yield item

    @staticmethod
    def launch_task(fn, user_id: int, *args,
                    description=None, field: str = None,
                    **kwargs):
        from flask import current_app

        if isinstance(fn, Callable):
            name = fn.__name__
        else:
            name = fn

        rq_job = current_app.task_queue.enqueue(fn, user_id, *args, **kwargs)

        new_session = db.create_session({})

        with new_session() as session:
            task = Task()
            task.id = rq_job.get_id()
            task.name = name
            task.description = description
            task.field = field
            task.owner_id = user_id

            session.add(task)
            session.commit()
