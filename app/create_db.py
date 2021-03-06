from datetime import date
import logging
import csv
from yaspin import yaspin
import click
from dataclasses import dataclass, make_dataclass
from app.models import EventModel
from flask import current_app
from flask.cli import with_appcontext
from app import db
from typing import Any, Iterable


# TODO: is this unnecessarily complicated?
def get_dataclass(headers: Iterable) -> Any:
    BaseDataClass: Any = make_dataclass('BaseDataClass',
                                        [item.strip() for item in
                                         headers])  # noqa

    @dataclass
    class EventDataclass(BaseDataClass):
        def __post_init__(self):
            self.stars = int(self.stars)  # noqa
            self.timestamp = date.fromtimestamp(int(self.timestamp))  # noqa

    return EventDataclass


def read_csv(file):
    with open(file) as csv_file:
        event_reader = csv.reader(csv_file, delimiter=';')
        headers = next(event_reader)
        EventDataclass = get_dataclass(headers)  # noqa
        for row in event_reader:
            try:
                row_to_base = EventDataclass(*row)
                yield row_to_base
            except ValueError as e:
                logging.warning(
                    f'\n{e} in line {event_reader.line_num}: '
                    f'{row} \nrow skipped')


def init_db():
    db.drop_all()
    db.create_all()
    file2 = current_app.config.get('SOURCE_PATH')
    all_events = read_csv(file=file2)
    events_db = []
    with yaspin(text="Loading", color="green") as spinner:
        for event in all_events:
            events_db.append(EventModel(
                id=event.id,
                asin=event.asin,
                brand=event.brand,
                source=event.source,
                stars=event.stars,
                timestamp=event.timestamp
            ))
        spinner.ok("✅ ")
    db.session.add_all(events_db)
    db.session.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('\nDatabase is initialized.')


def init_app(app):
    app.cli.add_command(init_db_command)
