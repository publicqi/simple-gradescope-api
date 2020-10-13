from bs4 import BeautifulSoup
try:
    from assignment import GSAssignment
except ModuleNotFoundError:
    from .assignment import GSAssignment
from dateutil import parser

class GSCourse():

    def __init__(self, cid, name, shortname, year, session):
        self.cid = cid
        self.name = name
        self.shortname = shortname
        self.year = year
        self.session = session
        self.assignments = {}
        self.load_assignments()

    def load_assignments(self):
        assignment_resp = self.session.get(
            'https://www.gradescope.com/courses/' + self.cid)
        parsed_assignment_resp = BeautifulSoup(assignment_resp.text, 'html.parser')

        data_table_tbody = parsed_assignment_resp.find('tbody')
        assignment_entries = list(data_table_tbody.findAll('tr'))
        for assignment in assignment_entries:
            name_th = assignment.find('th')
            if name_th.find('a'):
                name = name_th.find('a').string
            else:
                name = name_th.find('button').string

            status = assignment.find('div', class_='submissionStatus--text').string
            released_ts = parser.parse(assignment.findAll('td', class_='hidden-column')[0].string)
            due_ts = parser.parse(assignment.findAll('td', class_='hidden-column')[1].string)

            self.assignments[name] = GSAssignment(name, status, released_ts, due_ts)

    def get_dues(self):
        pass
