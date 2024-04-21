# my_app/tasks.py

from celery import shared_task

@shared_task
def my_daily_task():
    print("Running my daily task!")
