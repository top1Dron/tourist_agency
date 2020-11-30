from datetime import datetime
from config.celery import app

from .service import backup_database, print_message, export_models_to_excel


@app.task
def regular_backup_database():
    backup_database()


@app.task
def task_hello(date=f'Hello World'):
    print_message(date)


@app.task
def task_export_db_to_excel():
    return export_models_to_excel()