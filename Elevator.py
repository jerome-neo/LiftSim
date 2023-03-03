from enum import Enum
import random
MAX_CAPACITY = 8
MAX_WEIGHT = 1600 # kilograms
SPEED = (0.5, 0.6)
DIRECTION = Enum('Direction', ['UP', 'DOWN'])


class Elevator(object):
    def __init__(self, index, collection_floors, curr_floor):
        self.index = index
        self.floors = collection_floors
        self.max_persons = MAX_CAPACITY
        self.max_weight = MAX_WEIGHT
        self.curr_floor = curr_floor
        self.speed = SPEED  # metres per second
        self.direction = DIRECTION.UP
        self.is_door_open = False
        self.is_servicing = False
        self.passengers = []

    def __str__(self):
        return f"Elevator at {self.curr_floor} with {len(self.passengers)} person(s) going {self.direction}"

    def add_passengers(self, person):
        self.passengers.append(person)

    def enter_elevator(self):
        yield self.env.timeout(random.randint(2, 4))

    def leave_elevator(self):
        yield self.env.timeout(random.randint(2, 4))

