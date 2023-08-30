import os
#import settings
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_rrhh.settings')

app = Celery('app_rrhh')
app.conf.enable_utc = False
app.conf.update(timezone = 'America/Lima')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
#app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-mail-every-day': {
        'task' : 'main.tasks.send_notification',
        'schedule' : crontab(hour=9 ,minute='42'),
        #'options' : {
        #    'expires' : 60.0,
        #},8
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')