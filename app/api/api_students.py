from random import choice
from flask_restx import Resource, Api, fields, abort
from sqlalchemy import and_
from app.api import bp_api
from app.models import StudentModel, CourseModel
from app import db, csrf
from app.main.common_funcs import filter_groups_by_size, search_student_query


api = Api(bp_api, version='1.0', title="Students", description='A simple students API', decorators=[csrf.exempt])
ns = api.namespace('students', description='Students operations')

student_model = api.model('Student', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'group': fields.String,
    'courses': fields.List(fields.String)
})


get_parser = api.parser()
get_parser.add_argument('first_name', type=str)
get_parser.add_argument('last_name', type=str)
get_parser.add_argument('group', choices=StudentModel.all_groups)
get_parser.add_argument('course', choices=StudentModel.all_courses)

post_parser = api.parser()
post_parser.add_argument('first_name', type=str, required=True, help="First name cannot be blank!")
post_parser.add_argument('last_name', type=str, required=True, help="Last name cannot be blank!")


def check_course(action, course, student) -> bool:
    """ Check is course can be added or deleted for current student."""
    checks = {
        'append': course in student.get_av_courses(),
        'remove': course in CourseModel.query.with_parent(student).all()
    }
    return checks.get(action, False)


@ns.route('/')
class StudentList(Resource):

    @ns.expect(get_parser)
    @ns.marshal_list_with(student_model)
    def get(self):
        """ Get all students or search students by first_name, last_name, group, course.
        Any number of parameters can be passed, or neither.
        """
        args = get_parser.parse_args()
        queries = search_student_query(args)
        data = StudentModel.query.filter(and_(*queries)).order_by('id').all()
        return data

    @ns.expect(post_parser)
    @ns.marshal_with(student_model, code=201)
    def post(self):
        """ Create a new student."""
        data = post_parser.parse_args()
        available_groups = filter_groups_by_size(29, 9)
        group = choice(available_groups)
        new_student = StudentModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
            group_id=group.id)
        db.session.add(new_student)
        db.session.commit()
        return new_student, 201


@ns.route('/<int:student_id>')
@ns.response(404, 'Student not found')
@ns.param('student_id', 'The student identifier')
class Student(Resource):

    put_parser = api.parser()
    put_parser.add_argument('action', choices=['append', 'remove'], help="Append(add) or remove an course.")
    put_parser.add_argument('course', choices=StudentModel.all_courses,
                            help="Course being processed.")

    @ns.doc('get_student')
    @ns.marshal_with(student_model)
    def get(self, student_id):
        """ Show a single student by id."""
        current_student = StudentModel.query.get_or_404(student_id)
        return current_student

    @ns.doc('delete_student')
    @ns.response(204, 'Student deleted')
    def delete(self, student_id):
        """ Delete a student given its identifier."""
        current_student = StudentModel.query.get_or_404(student_id)
        db.session.delete(current_student)
        db.session.commit()
        return '', 204

    @ns.expect(put_parser)
    @ns.marshal_with(student_model)
    def put(self, student_id):
        """ Update a student's course."""
        student = StudentModel.query.get_or_404(student_id)
        action, course_name = self.put_parser.parse_args().values()
        course = CourseModel.query.filter_by(name=course_name).first_or_404()
        if check_course(action, course, student):
            getattr(student.courses, action)(course)
            db.session.commit()
            return student
        error_message = f'You can`t {action} {course.name} for {student.first_name} {student.last_name} student.'
        return abort(400, message=error_message)
