from flask_restx import Resource, Api, fields
from sqlalchemy import and_, func, desc
from app.api import bp_api
from app.models import EventModel


api = Api(bp_api, version='1.0', title="Simporter", description='A Simporter API')
ns = api.namespace('api', description='Events operations')

parser = api.parser()
parser.add_argument(
    "startDate", type=str, required=True, help="Start date", location='args'
)
parser.add_argument(
    "endDate", type=str, required=True, help="Start date", location='args'
)
parser.add_argument('Type', choices=('cumulative', 'usual'))
parser.add_argument('Grouping', choices=('weekly', 'bi-weekly', 'monthly'))


@ns.route('/info')
class FilteringInfo(Resource):

    def get(self):
        """Get  Information about possible filtering (list of attributes and list of values for each attribute)"""
        start_date = EventModel.query.order_by('timestamp').first().timestamp.isoformat()
        end_date = EventModel.query.order_by(desc('timestamp')).first().timestamp.isoformat()
        data_type = ('cumulative', 'usual')
        grouping = ('weekly', 'bi-weekly', 'monthly')
        filters = ('attributes', 'values')
        data = {'startDate': start_date,
                'endDate': end_date,
                'Type': data_type,
                'Grouping': grouping,
                'Filters': filters}
        return data


# TODO: add parser for filters

@ns.route('/timeline')
class Timeline(Resource):
    @api.doc(parser=parser)
    def get(self):
        """ Show a timeline by param."""
        args = parser.parse_args()
        filters = {
            # 'asin': 'B0014D3N0Q',
            # 'brand': 'Downy',
            # 'source': 'amazon',
            # 'stars': 5
        }

        output_data = EventModel.query \
            .with_entities(*get_entities(args['Type'])) \
            .filter(and_(*get_period(args['startDate'], args['endDate']), *get_attributes(filters))) \
            .group_by(*get_grouping(args['Grouping']))\
            .order_by(EventModel.timestamp)\
            .all()
        return {'timeline': [r._asdict() for r in output_data]}


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
    grouping_dict = {'bi-weekly': (func.strftime('%W', EventModel.timestamp))/2,
                     'monthly': func.strftime('%m', EventModel.timestamp)}
    return (func.strftime('%Y', EventModel.timestamp),
            grouping_dict.get(grouping,
                             func.strftime('%W', EventModel.timestamp)))


def get_attributes(filters=None):
    queries = ((getattr(EventModel, key) == value) for key, value in filters.items())
    return queries



"""
SELECT strftime('%W-%Y', timestamp) AS  WeekNumber,
       COUNT(id) AS Events,
       SUM(COUNT(id)) OVER (order by timestamp) as Sum,
       timestamp
FROM event_model
WHERE timestamp BETWEEN '2019-01-01' AND
datetime('2019-01-01', '+9 months')
GROUP BY WeekNumber
ORDER BY WeekNumber"""