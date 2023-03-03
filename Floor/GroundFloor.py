import Floor


class GroundFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_up_persons = []

    def add_person(self, person):
        self.going_up_persons.append(person)

    def remove_all_persons_going_up(self):
        self.going_up_persons = []
