from bs4 import BeautifulSoup
from dateutil import parser
from datetime import datetime

class GSCourse():

    def __init__(self, cid, name, shortname, year, session):
        self.cid = cid
        self.name = name
        self.shortname = shortname
        self.year = year
        self.session = session
        self.assignments = []

    def load_assignments(self):
        self.assignments = []
        assignment_resp = self.session.get(
            'https://www.gradescope.com/courses/' + self.cid)
        parsed_assignment_resp = BeautifulSoup(
            assignment_resp.text, 'html.parser')

        data_table_tbody = parsed_assignment_resp.find('tbody')
        assignment_entries = list(data_table_tbody.findAll('tr'))
        for assignment in assignment_entries:
            name_th = assignment.find('th')
            if name_th.find('a'):
                name = name_th.find('a').string
            elif name_th.find('button'):
                name = name_th.find('button').string
            else:
                name = name_th.string

            status = assignment.find(
                'div', class_='submissionStatus--text').string
            released_ts = int(parser.parse(assignment.findAll(
                'td', class_='hidden-column')[0].string).timestamp())
            due_ts = int(parser.parse(assignment.findAll(
                'td', class_='hidden-column')[1].string).timestamp())
            current_ts = int(datetime.now().timestamp())

            self.assignments.append(
                {'name': name, 'status': status, 'released_ts': released_ts, 'due_ts': due_ts, 'current_ts': current_ts})

    def get_dues(self):
        self.load_assignments()
        return self.assignments
