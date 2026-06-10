import asyncio

from celery import Task


class BaseTask(Task):
    """Base class for managing the execution of asynchronous tasks in Celery."""

    def __call__(self, *args, **kwargs):
        # Gets the existing and active event loop in the Worker's process
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()

        # Runs the native coroutine until it finishes, using the correct loop
        return loop.run_until_complete(self.run(*args, **kwargs))
