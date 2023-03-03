import random


class Person(object):
    def __init__(self, env):
        self.env = env
        self.curr_floor = random.int(1, 10)
        self.destination_floor = random.choice(list(set([i for i in range(1, 10)]) - set(self.curr_floor)))
        self.arrival_time = env.now
        self.end_time = None

    def calls_elevator(self):
        yield self.env.timeout(1)

    def has_reached_destination(self, elevator):
        return elevator.curr_floor == self.destination_floor

    def complete_trip(self):
        self.end_time = self.env.now

    def get_wait_time(self):
        time_taken_to_complete = self.env_time - self.arrival_time
        return time_taken_to_complete

    def get_curr_floor(self):
        return self.curr_floor

    def get_dest_floor(self):
        return self.destination_floor

    def get_direction(self):
        return -1 if self.curr_floor > self.destination_floor else 1

