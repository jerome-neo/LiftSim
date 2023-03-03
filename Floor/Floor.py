class Floor(object):
    def __init__(self, index):
        self.floor_index = index
        self.call_up = False
        self.call_down = False

    def __str__(self):
        return "Floor {self.floor_index}"

    def has_call_down(self):
        return self.call_down

    def has_call_up(self):
        return self.call_up

    def call_up(self):
        self.call_up = True

    def call_down(self):
        self.call_down = True

    def uncall_up(self):
        self.call_up = False

    def uncall_down(self):
        self.call_down = False

    def get_floor_level(self):
        return self.floor_index
