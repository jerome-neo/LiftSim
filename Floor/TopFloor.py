from .Floor import Floor


class TopFloor(Floor):
    def __init__(self, index):
        super().__init__(index)
        self.going_down_persons = []

    def __str__(self):
        return f"Top floor has {len(self.going_down_persons)} person(s) going down. Button pressed? {self.call_down}"

    def add_person_going_down(self, person):
        self.going_down_persons.append(person)

    def remove_all_persons_going_down(self):
        pointer = []
        n = len(self.going_down_persons)
        for i in range(n):
            pointer.append(self.going_down_persons.pop())
        return pointer

