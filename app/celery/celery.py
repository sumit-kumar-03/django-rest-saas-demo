import os
from celery import Celery
from app.logger import logger


BROKER_URL = "{schema}://{username}:{password}@{host}:{port}//".format(
    schema=os.getenv(
        "RABBITMQ_SCHEMA",
        "amqp",
    ),
    username=os.getenv(
        "RABBITMQ_USERNAME",
        "guest",
    ),
    password=os.getenv(
        "RABBITMQ_PASSWORD",
        "guest",
    ),
    host=os.getenv(
        "RABBITMQ_HOST",
        "rabbitmq",
    ),
    port=os.getenv(
        "RABBITMQ_PORT",
        5672,
    ),
)


def create_celery_app() -> Celery:
    """Create and configure the Celery application"""
    logger.info("Started creating celery app")

    app = Celery(
        "saas_project_celery_app",
        broker=BROKER_URL,
    )

    # Configure broker connection retry
    app.conf.broker_connection_retry = True
    app.conf.broker_connection_retry_on_startup = True
    app.conf.broker_connection_max_retries = 10

    # Configure broker heartbeat and timeouts
    app.conf.broker_heartbeat = 30
    app.conf.broker_connection_timeout = 60

    # Worker settings
    app.conf.worker_prefetch_multiplier = 4
    app.conf.worker_max_tasks_per_child = 1000

    # Task settings
    app.conf.task_acks_late = True
    app.conf.task_reject_on_worker_lost = True

    # Tasks
    app.autodiscover_tasks(
        [
            "app.celery.tasks",
            "app.billing.tasks",
        ]
    )

    return app


saas_project_celery_app = create_celery_app()
logger.info("Finished creating celery app")
