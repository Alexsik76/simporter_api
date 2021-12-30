from sqlalchemy import and_, func, desc
from flask_restx import Resource, Api, marshal, reqparse, fields

from app.api import bp_api
from app.models import EventModel

api = Api(bp_api, version='1.0', title="Simporter", description='A Simporter API')
ns = api.namespace('api', description='Base API')


ATTR_LIST = 'asin', 'brand', 'source', 'stars'


class FromTupleString(fields.Raw):
    def format(self, value):
        return value[0]


attr_fields = {attr: fields.List(FromTupleString) for attr in ATTR_LIST}


@ns.route('/info')
class FilteringInfo(Resource):
    def get(self): # noqa
        """Get  Information about possible filtering (list of attributes and list of values for each attribute)"""
        start_date = EventModel.query.order_by('timestamp').first().timestamp.isoformat()
        end_date = EventModel.query.order_by(desc('timestamp')).first().timestamp.isoformat()
        data = [{'startDate': [start_date, end_date]},
                {'endDate': [start_date, end_date]},
                {'Type': ['cumulative', 'usual']},
                {'Grouping': ['weekly', 'bi-weekly', 'monthly']},
                {'Filters': get_distinct_values()}]
        return data


def get_distinct_values():
    data = {attr: EventModel.query.with_entities(getattr(EventModel, attr)).distinct() for attr in ATTR_LIST}
    return marshal(data, attr_fields)


parser = reqparse.RequestParser()

parser.add_argument("startDate", type=str, required=True, help="Start date")
parser.add_argument("endDate", type=str, required=True, help="End date")

parser.add_argument('Type', choices=('cumulative', 'usual'))
parser.add_argument('Grouping', choices=('weekly', 'bi-weekly', 'monthly'),
                    help='weekly - (data for each week), '
                         'bi-weekly - (data for each 2 weeks), '
                         'monthly (data for each month)')

parser.add_argument('asin', type=str, help="Amazon Standard Identification Number")
parser.add_argument('brand', type=str, help="Brand")
parser.add_argument('source', type=str, help="Source")
parser.add_argument('stars', type=str, help="Stars")

event_model = api.model('Event', {
    'date': fields.Date,
    'value': fields.Integer}
                        )


@ns.route('/timeline')
class Timeline(Resource):

    @api.marshal_with(event_model, envelope='timeline')
    @api.doc(parser=parser)
    def get(self):
        """ Show a timeline by param."""
        args = parser.parse_args()
        output_data = EventModel.query \
            .with_entities(*get_entities(args['Type'])) \
            .filter(and_(*get_period(args['startDate'], args['endDate']), *get_attributes(args))) \
            .group_by(*get_grouping(args['Grouping'])) \
            .order_by(EventModel.timestamp) \
            .all()
        return output_data


def get_entities(key=None):
    data_types_dict = {
        'cumulative': func.sum(func.count(EventModel.id)).over(order_by=EventModel.timestamp).label('value')
    }
    return (func.date(EventModel.timestamp).label('date'),
            data_types_dict.get(key,
                                func.count(EventModel.id).label('value')))


def get_period(start_date, end_date):
    filtered_period = (
        EventModel.timestamp >= start_date,
        EventModel.timestamp <= end_date
    )
    return filtered_period


def get_grouping(grouping=None):
    grouping_dict = {'bi-weekly': (func.strftime('%W', EventModel.timestamp)) / 2,
                     'monthly': func.strftime('%m', EventModel.timestamp)}
    return (func.strftime('%Y', EventModel.timestamp),
            grouping_dict.get(grouping,
                              func.strftime('%W', EventModel.timestamp)))


def get_attributes(args):
    attributes = {key: value for key, value in args.items() if key in ATTR_LIST}
    queries = ((getattr(EventModel, key) == value) for key, value in attributes.items() if value)
    return queries
