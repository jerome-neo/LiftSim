from copy import deepcopy
from .Floor import Floor


class GroundFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_up_persons = []

    def __str__(self):
        return f"Ground floor has {len(self.going_up_persons)} person(s) going up. Button pressed? {self.call_up}"

    def add_person_going_up(self, person):
        self.going_up_persons.append(person)

    def remove_all_persons_going_up(self):
        pointer = []
        n = len(self.going_up_persons)
        for i in range(n):
            pointer.append(self.going_up_persons.pop())
        return pointer
