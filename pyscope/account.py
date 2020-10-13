try:
    from course import GSCourse
except ModuleNotFoundError:
    from .course import GSCourse


class GSAccount():
    '''A class designed to track the account details (instructor and student courses'''

    def __init__(self, email, session):
        self.email = email
        self.session = session
        self.student_courses = {}

    def add_class(self, cid, name, shortname, year):
        self.student_courses[cid] = GSCourse(cid, name, shortname, year, self.session)

    def get_dues(self, year):
        dues = {}
        for cid in self.student_courses.keys():
            if self.student_courses[cid].year == year:
                dues[cid] = self.student_courses[cid].get_dues()
        return dues
