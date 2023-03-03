from copy import deepcopy
import Floor


class SandwichFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_up_persons = []
        self.going_down_persons = []

    def add_person_going_up(self, person):
        self.going_up_persons.append(person)

    def add_person_going_down(self, person):
        self.going_down_persons.append(person)

    def remove_all_persons_going_up(self):
        copy = deepcopy(self.going_up_persons)
        self.going_up_persons.clear()
        return copy

    def remove_all_persons_going_down(self):
        copy = deepcopy(self.going_down_persons)
        self.going_down_persons.clear()
        return copy
