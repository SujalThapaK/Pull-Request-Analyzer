from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
app.autodiscover_tasks(["app"])
app.conf.broker_connection_retry_on_startup = True
app.conf.update(task_serializer="json", accept_content=["json"])