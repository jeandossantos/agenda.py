from celery import Celery
import os

# precisa dizer qual settings deve ser usando para encontrar os app instalados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings.development')

app = Celery('_core')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task
def soma(a, b):
    import time
    time.sleep(10)
    return a + b
