from enum import Enum
from copy import deepcopy
import heapq
import random
MAX_CAPACITY = 8
MAX_WEIGHT = 1600 # kilograms
SPEED = (0.5, 0.6)
DIRECTION = Enum('Direction', ['UP', 'DOWN'])


class Elevator(object):
    def __init__(self, env, index, collection_floors, curr_floor, direction):
        self.env = env
        self.index = index
        self.floors = collection_floors
        self.direction = DIRECTION.UP if direction == "UP" else DIRECTION.DOWN
        self.max_persons = MAX_CAPACITY  # not implemented
        self.max_weight = MAX_WEIGHT  # not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_busy = False
        self.passengers = []
        self.path = []  # empty heap

    def __str__(self):
        return f"Elevator at {self.curr_floor} with {len(self.passengers)} person(s) going {self.direction}"

    def get_current_floor(self):
        return self.curr_floor

    def add_passengers(self, person):
        self.passengers.append(person)

    def enter_elevator(self, list_of_person):
        for person in list_of_person:
            self.passengers.add_passenger(person)
            floor_level = person.get_dest_floor()
            # Add items to the heap (priority, value)
            self.path.append(floor_level)
        self.path.sort()
        yield self.env.timeout(random.randint(2, 4))

    def leave_elevator(self):
        copy = deepcopy(self.passengers)
        for person in copy:
            if person.get_dest_floor() == self.curr_floor:
                person.complete_trip()
                self.passengers.remove(person)
        yield self.env.timeout(random.randint(2, 4))

    def is_busy(self):
        return self.is_busy

    def set_idle(self):
        self.is_busy = False

    def travel(self, end):
        self.curr_floor = end
        yield self.env.timeout(abs(end - self.curr_floor) * 3)

    def add_path(self, floor_level):
        self.path.append(floor_level)
        self.path.sort()

    def get_path(self):
        return self.path

    def has_path(self):
        return len(self.path) != 0






