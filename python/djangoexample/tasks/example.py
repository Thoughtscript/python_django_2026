from django.tasks import task

@task
def log_note(msg):
    print(f"Task received with note: {msg}")
    return "Task completed!"