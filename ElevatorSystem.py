import Elevator


class ElevatorSystem(object):
    def __init__(self, env, collection_floors, num_up, num_down):
        self.env = env
        self.floors = collection_floors
        self.elevators_up = [Elevator.Elevator(env, i, self.floors, 1, "UP") for i in range(1, num_up + 1)]
        self.elevators_down = [Elevator.Elevator(env, i, self.floors, 1, "DOWN") for i in range(1, num_down + 1)]

    def handle_person(self, person):
        # Put the person in the floor and call the lift
        call_direction = person.get_direction()
        curr_floor = self.floors[person.get_curr_floor() - 1]
        if call_direction < 0:
            curr_floor.add_person_going_down(person)
            curr_floor.call_down()
        else:
            curr_floor.add_person_going_up(person)
            curr_floor.call_up()

    def handle_landing_call(self):
        # Return down elevators to repond to a landing call
        pass
    def activate_elevators(self):

        # Look for the landing call from the highest floor
        pass
