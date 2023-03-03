import Floor


class SandwichFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_up_persons = []
        self.going_down_persons = []

    def add_person_going_up(self, person):
        self.going_up_persons.append(person)

    def add_person_going_down(self, person):
        self.going_down_persons

    def remove_all_persons_going_up(self):
        self.going_up_persons = []

    def remove_all_persons_going_down(self):
        self.going_down_persons = []
