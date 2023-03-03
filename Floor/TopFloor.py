import Floor


class TopFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_down_persons = []

    def add_person(self, person):
        self.going_down_persons.append(person)

    def remove_all_persons_going_down(self):
        self.going_down_persons = []

