import datetime
import os
import csv
import click
from dataclasses import make_dataclass
from app.models import EventModel
from flask.cli import with_appcontext
from yaspin import yaspin
from app import db


def read_csv(file):
    with open(file) as csv_file:
        event_reader = csv.reader(csv_file, delimiter=';')
        headers = next(event_reader)
        event_class = make_dataclass('EventItem', [item.strip() for item in headers])
        for row in event_reader:
            yield event_class(*row)


def init_db():
    db.drop_all()
    print('All tables are dropped.')
    db.create_all()
    print('Created new tables.')
    print('...')
    dirname = os.path.dirname(__file__)
    file = os.path.join(dirname, '../source_data/data.csv')
    all_events = read_csv(file=file)
    events_db = []
    with yaspin(text="Storing data from file to database...", color="green", timer=True) as spinner:
        for event in all_events:
            events_db.append(EventModel(
                id=event.id,
                asin=event.asin,
                brand=event.brand,
                source=event.source,
                stars=int(event.stars),
                timestamp=datetime.datetime.fromtimestamp(int(event.timestamp))
            ))
        db.session.add_all(events_db)
        db.session.commit()
        spinner.ok('✅')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('\nDatabase is initialized.')


def init_app(app):
    app.cli.add_command(init_db_command)
