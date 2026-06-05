import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates a session-scoped event loop compliant with Python 3.14+
    to support asynchronous component testing.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
