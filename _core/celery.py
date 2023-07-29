from celery import Celery
import os

# precisa dizer qual settings deve ser usando para encontrar os app instalados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings.development')

app = Celery('_core', broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

app.autodiscover_tasks()


@app.task
def soma(a, b):
    import time
    time.sleep(10)
    return a + b
