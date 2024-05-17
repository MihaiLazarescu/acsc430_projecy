from project_main.celery import app
import time
from django.core.management import call_command
from .utils import send_email_notofication
from django.conf import settings


@app.task
def celery_test_task():
    time.sleep(10)
    mail_subject = 'Test subject'
    message = 'Test message'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notofication(mail_subject, message, to_email)

    return 'Email send successfully'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e
    mail_subject = 'Import data Completed'
    message = 'Your data has been imported'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notofication(mail_subject, message, to_email)
    return 'Data imported successfully'
    