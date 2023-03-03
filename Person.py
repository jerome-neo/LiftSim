import random


class Person(object):
    def __init__(self, env, index, building):
        self.id = index
        self.env = env
        self.curr_floor = random.randint(1, building.get_num_floors()//3)
        self.destination_floor = \
            random.choice(list(set([i for i in range(1, building.get_num_floors() + 1)]) - set([self.curr_floor])))
        self.arrival_time = env.now
        self.end_time = None
        self.has_reached_floor = False

    def __str__(self):
        return f"Person {self.id} starting at {self.curr_floor} and going to {self.destination_floor}:"

    def calls_elevator(self):
        yield self.env.timeout(1)

    def has_reached_destination(self, elevator):
        return elevator.get_current_floor() == self.destination_floor

    def complete_trip(self):
        self.end_time = self.env.now
        self.has_reached_floor = True

    def has_completed_trip(self):
        return self.has_reached_floor

    def get_wait_time(self):
        time_taken_to_complete = self.end_time - self.arrival_time
        return time_taken_to_complete

    def get_curr_floor(self):
        return self.curr_floor

    def get_dest_floor(self):
        return self.destination_floor

    def get_direction(self):
        return -1 if self.curr_floor > self.destination_floor else 1

