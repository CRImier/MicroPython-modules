import pyb

class Car():
    def __init__(self):
        self.sensors = None
        self.actuators = None
        self.goals = None

    def setup(self):
        for setup_action in self.setup_actions:
            if len(setup_action) == 2:
                setup_action[0](*setup_action[1])
            else:
                setup_action[0]()

    def run(self):
        while True:
            for goal in self.goals:
                if goal[0]():
                    goal[1]()

