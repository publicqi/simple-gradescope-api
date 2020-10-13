class GSAssignment():

    def __init__(self, name, status, released, due, current):
        '''Create a assignment object'''
        self.name = name
        self.status = status
        self.released = released
        self.due = due
        self.time_left = due - current