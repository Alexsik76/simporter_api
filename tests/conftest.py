import os
import tempfile

import pytest

from app import create_app


@pytest.fixture(scope='session')
def app(request):
    app = create_app(test_config=True)
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            from app.create_db import init_app
            init_app(app)
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def runner(app):

    return app.test_cli_runner()
