from app import db


class EventModel(db.Model):
    id = db.Column(db.String(15), primary_key=True)
    asin = db.Column(db.String(15), index=True)
    brand = db.Column(db.String(25), index=True)
    source = db.Column(db.String(15), index=True)
    stars = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True)

    def __repr__(self):
        return self.id

    def __str__(self):
        return f'{self.id}: {self.timestamp}'


# class StudentModel(db.Model):
#     all_groups = []
#     all_courses = []
#
#     @classmethod
#     def get_all_groups_and_courses(cls):
#         cls.all_groups = [item[0] for item in GroupModel.query.with_entities(GroupModel.name).all()]
#         cls.all_courses = [item[0] for item in CourseModel.query.with_entities(CourseModel.name).all()]
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(24), index=True)
#     last_name = db.Column(db.String(24), index=True)
#     courses = db.relationship('CourseModel', secondary=courses, lazy='subquery',
#                               backref=db.backref('students', lazy=True))
#     group_id = db.Column(db.Integer, db.ForeignKey('group_model.id'))
#
#     def __repr__(self):
#         return f'<Student {self.first_name} {self.last_name}\n' \
#                f'Group {self.group.name}\n>'
#
#     def __str__(self):
#         courses_str = [course.name for course in self.courses]
#         return f'{self.first_name} {self.last_name} {self.group.name} {courses_str}'
#
#     def get_av_courses(self):
#         my_courses = CourseModel.query\
#             .with_parent(self)\
#             .with_entities(CourseModel.id)
#         av_courses = CourseModel.query\
#             .filter(CourseModel.id.notin_(my_courses)).all()
#         return av_courses
