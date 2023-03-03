from copy import deepcopy
from .Floor import Floor


class SandwichFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_up_persons = []
        self.going_down_persons = []

    def __str__(self):
        return f"Floor {self.floor_index} has " \
               f"{len(self.going_up_persons)} person(s) going up and " \
               f"{len(self.going_down_persons)} person(s) going down. Buttons pressed? {self.call_up} {self.call_down}"

    def add_person_going_up(self, person):
        self.going_up_persons.append(person)

    def add_person_going_down(self, person):
        self.going_down_persons.append(person)

    def remove_all_persons_going_up(self):
        pointer = []
        n = len(self.going_up_persons)
        for i in range(n):
            pointer.append(self.going_up_persons.pop())
        return pointer

    def remove_all_persons_going_down(self):
        pointer = []
        n = len(self.going_down_persons)
        for i in range(n):
            pointer.append(self.going_down_persons.pop())
        return pointer
