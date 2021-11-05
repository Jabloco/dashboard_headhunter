from celery import Celery

from webapp import app
import db_worker

flask_app = app
celery_app = Celery('tasks', broker=('redis://localhost:6379/0'))

@celery_app.task
def db_fill():
    with flask_app.app_context():
        db_worker
