"""Taskiq application configuration."""

from taskiq import TaskiqScheduler
from taskiq.schedule_sources.label_based import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.core.config import settings

# Create Taskiq broker with Redis
broker = ListQueueBroker(
    url=settings.TASKIQ_BROKER_URL,
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=settings.TASKIQ_RESULT_BACKEND,
    )
)

# Import scheduled tasks so they register on the broker
from app.worker.tasks import schedules  # noqa: F401

# Create scheduler for periodic tasks
# LabelScheduleSource scans the broker for tasks with @broker.task(schedule=[...])
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


# Startup/shutdown hooks
@broker.on_event("startup")
async def startup() -> None:
    """Initialize broker on startup."""
    pass


@broker.on_event("shutdown")
async def shutdown() -> None:
    """Cleanup on shutdown."""
    pass
