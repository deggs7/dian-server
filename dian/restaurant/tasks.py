from celery import task


@task
def add(x, y):
    return x + y


@task
def send_msg(msg_task):
    print msg_task.registration.queue_number
