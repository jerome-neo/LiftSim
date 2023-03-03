from enum import Enum
from copy import deepcopy
import heapq
import random
MAX_CAPACITY = 8
MAX_WEIGHT = 1600 # kilograms
SPEED = (0.5, 0.6)


class Elevator(object):
    def __init__(self, env, index, collection_floors, curr_floor, direction):
        self.env = env
        self.index = index
        self.floors = collection_floors
        self.direction = direction
        self.max_persons = MAX_CAPACITY  # not implemented
        self.max_weight = MAX_WEIGHT  # not implemented
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.is_working_status = False
        self.passengers = []
        self.path = []  # empty heap

    def __str__(self):
        return f"elevator dedicated to {self.direction} calls is at " \
               f"{self.curr_floor} with {len(self.passengers)} person(s)"

    def get_direction(self):
        return self.direction

    def get_current_floor(self):
        return self.curr_floor

    def add_passengers(self, person):
        self.passengers.append(person)

    def enter_elevator(self, list_of_person):
        for person in list_of_person:
            self.add_passengers(person)
            floor_level = person.get_dest_floor()
            # Add items to the heap (priority, value)
            self.path.append(floor_level)
            print(f"{person} has entered {self}")
        self.path.sort()
        yield self.env.timeout(random.randint(2, 4))

    def leave_elevator(self):
        to_remove = []
        for person in self.passengers:
            if person.has_reached_destination(self):
                person.complete_trip()
                to_remove.append(person)
                print(f"{person} has left {self}")
        for person in to_remove:
            self.passengers.remove(person)
        yield self.env.timeout(random.randint(2, 4))

    def is_busy(self):
        return self.is_working_status

    def set_busy(self):
        self.is_working_status = True

    def set_idle(self):
        self.is_working_status = False

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






