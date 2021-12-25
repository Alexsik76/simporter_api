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
def runner(app):

    return app.test_cli_runner()
