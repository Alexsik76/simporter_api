from app import db


class EventModel(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    asin = db.Column(db.String(15), index=True)
    brand = db.Column(db.String(25), index=True)
    source = db.Column(db.String(15), index=True)
    stars = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.Date, index=True)

    def __repr__(self):
        return self.id

    def __str__(self):
        return f'{self.id}: {self.timestamp}'
