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
        # Return down elevators to respond to a landing call
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_down)):
                yield self.env.timeout(1)
            else:
                elevator = min(self.elevators_down, key=lambda x: x.get_current_floor())
                for floor in self.floors:
                    if floor.has_call_down():
                        elevator.add_path(floor.get_floor_level())

                break

    def move(self):
        for elevator in self.elevators_down:
            if elevator.get_path().isEmpty():
                elevator.set_idle()
            curr_floor = elevator.get_current_floor()
            adj_floor = curr_floor - 1;
            if adj_floor in elevator.get_path():
                next_floor = elevator.get_path().pop()  # remove from the back
                # take in passengers
                elevator.travel(next_floor)
                floor = self.floors[next_floor - 1]
                elevator.enter_elevator(floor.remove_all_persons_going_down())
                floor.uncall_down()

                # take out passengers if any
                elevator.leave_elevator()
        for elevator in self.elevators_up:
            pass

    def floors_with_down_calls(self):
        floors = []
        for i, floor in enumerate(self.floors):
            if floor.has_call_down():
                floors.append(i)
        return floors

    def floors_with_up_calls(self):
        floors = []
        for i, floor in enumerate(self.floors):
            if floor.has_call_up():
                floors.append(i)
        return floors
