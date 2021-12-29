from app.models import EventModel
from app import db, create_app
app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'StudentModel': EventModel}
