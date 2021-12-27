from random import choice
from flask_restx import Resource, Api, fields, abort
from sqlalchemy import and_
from app.api import bp_api
from app.models import EventModel
from app import db
from sqlalchemy import desc
# from app.main.common_funcs import filter_groups_by_size, search_student_query


api = Api(bp_api, version='1.0', title="Simporter", description='A Simporter API')
ns = api.namespace('events', description='Events operations')

student_model = api.model('EventModel', {
    'id': fields.String,
    'asin': fields.String,
    'brand': fields.String,
    'source': fields.String,
    'stars': fields.Integer,
    'timestamp': fields.Date,
})


get_parser = api.parser()
# get_parser.add_argument('first_name', type=str)
# get_parser.add_argument('last_name', type=str)
# get_parser.add_argument('group', choices=StudentModel.all_groups)
# get_parser.add_argument('course', choices=StudentModel.all_courses)

post_parser = api.parser()
post_parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank!")
post_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")


@ns.route('/info')
class FilteringInfo(Resource):

    # @ns.marshal_list_with(student_model)
    def get(self):
        """Get  Information about possible filtering (list of attributes and list of values for each attribute)"""
        start_date = EventModel.query.order_by('timestamp').first().timestamp.isoformat()
        end_date = EventModel.query.order_by(desc('timestamp')).first().timestamp.isoformat()
        type_date = ('cumulative', 'usual')
        grouping = ('weekly', 'bi - weekly', 'monthly')
        filters = ('attributes', 'values')
        data = {'startDate': start_date,
                'endDate': end_date,
                'Type': type_date,
                'Grouping': grouping,
                'Filters': filters}
        return data




# @ns.route('/<int:student_id>')
# @ns.response(404, 'Student not found')
# @ns.param('student_id', 'The student identifier')
# class Student(Resource):
#
#     put_parser = api.parser()
#     put_parser.add_argument('action', choices=['append', 'remove'], help="Append(add) or remove an course.")
#     put_parser.add_argument('course', choices=StudentModel.all_courses,
#                             help="Course being processed.")
#
#     @ns.doc('get_student')
#     @ns.marshal_with(student_model)
#     def get(self, student_id):
#         """ Show a single student by id."""
#         current_student = StudentModel.query.get_or_404(student_id)
#         return current_student
#
#     @ns.doc('delete_student')
#     @ns.response(204, 'Student deleted')
#     def delete(self, student_id):
#         """ Delete a student given its identifier."""
#         current_student = StudentModel.query.get_or_404(student_id)
#         db.session.delete(current_student)
#         db.session.commit()
#         return '', 204
#
#     @ns.expect(put_parser)
#     @ns.marshal_with(student_model)
#     def put(self, student_id):
#         """ Update a student's course."""
#         student = StudentModel.query.get_or_404(student_id)
#         action, course_name = self.put_parser.parse_args().values()
#         course = CourseModel.query.filter_by(name=course_name).first_or_404()
#         if check_course(action, course, student):
#             getattr(student.courses, action)(course)
#             db.session.commit()
#             return student
#         error_message = f'You can`t {action} {course.name} for {student.first_name} {student.last_name} student.'
#         return abort(400, message=error_message)
