import Elevator


class ModernEGCS(object):
    """
    A system for controlling a group of elevators in a building using ModernEGCS algorithm.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators (list of Elevator): The collection of elevators within the building system.
    """
    def __init__(self, env, collection_floors, num_elevators,w1,w2,w3):
        """
        Initializes a ModernEGCS.

        Args:
            env (simpy.Environment): The simulation environment.
            collection_floors (list of Floor): The collection of floors in the building.
            num_elevators (int): The number of elevators in the system.

        """
        self.env = env
        self.floors = collection_floors
        self.elevators = [Elevator.Elevator(env, i, self.floors, 1) for i in range(1, num_elevators + 1)]
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        

    def __str__(self):
        """
        Returns a string representation of the ElevatorSystem.

        Returns:
            str: A string representation of the ElevatorSystem.

        """
        return f"ModernEGCS with {len(self.elevators)} elevators."



    def handle_person(self, person) -> None:
        """
        Handles a person who wants to use the elevator system.

        Args:
            person (Person): The person who wants to use the elevator system.
        """
        # Put the person in the floor and call the lift
        call_direction = person.get_direction()
        curr_floor = self.floors[person.get_curr_floor() - 1]
        if call_direction < 0:
            curr_floor.add_person_going_down(person)
            curr_floor.set_call_down()
        else:
            curr_floor.add_person_going_up(person)
            curr_floor.set_call_up()
    


    def handle_landing_call(self) -> None:
        """Handles a landing call from a person who wants to go down."""
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_down)):
                yield self.env.timeout(1)
            else:
                list_of_elevators = sorted(self.elevators_down, key=lambda x: x.get_current_floor(), reverse=True)
                chosen_index = 0
                elevator = list_of_elevators[chosen_index]
                while elevator.is_busy():
                    chosen_index += 1
                    elevator = list_of_elevators[chosen_index]
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_down() and (floor.get_floor_level() not in elevator.path):
                        elevator.add_path(floor.get_floor_level())
                break

    def handle_rising_call(self) -> None:
        """Handles a rising call from a person who wants to go up."""
        while True:
            if all(map(lambda x: x.is_busy(), self.elevators_up)):
                yield self.env.timeout(1)
            else:
                list_of_elevators = sorted(self.elevators_up, key=lambda x: x.get_current_floor(), reverse=False)
                chosen_index = 0
                elevator = list_of_elevators[chosen_index]
                while elevator.is_busy():
                    chosen_index += 1
                    elevator = list_of_elevators[chosen_index]
                elevator.set_busy()
                for floor in self.floors:
                    if floor.has_call_up() and (floor.get_floor_level() not in elevator.path):
                        elevator.add_path(floor.get_floor_level())
                break
            
    def assign_call(self,person) -> Elevator:
        """Assigns hall call to the most suitable elevator based on HCPM method."""
        person_current_floor = person.get_curr_floor()
        all_elevator_cost=[]
        all_priority_cost=[]
        for elevator in self.elevators:
            elevator_id = elevator.get_index()
            elevator_current_floor = elevator.get_current_floor()
            cost = abs(elevator_current_floor-person_current_floor)
            elevator_cost = (elevator_id,cost)
            all_elevator_cost.append(elevator_cost)
        all_elevator_cost.sort(key=lambda x: x[1])
            
        for i in range(len(self.elevators)-1):
            priority_cost=all_elevator_cost[i+1][1]-all_elevator_cost[i][1]
            elevator_id=
            all_priority_cost.append(priority_cost)

        #append all_priority_cost to global list for all unserved calls
        #if there are other lists in global list, sort such that the frontmost element gets its best elevator
        #else take the first elevator in the list
        
    def calculate_cost1(self,elevator) -> list:
        """
        Creates HCPM array used for deciding prioritization of hall calls.
        Cost = w1*sigma i: waiting passengers(WTi^2+RWTi^2) + w2* sigma i: riding passengers(RTi^2) + w3*PC
        Waiting Passengers = Passengers currently at the floor where elevator is, who will enter at this floor
        Riding Passengers = Passengers that are already inside the elevator, including those who alight at this floor
        """
        cost = 0
        if not elevator.is_moving():
            waiting_passengers_cost = 0
            floor = elevator.get_current_floor_object()
            if elevator.get_direction() == "UP":
                list_of_person = floor.get_all_persons_going_up()
            else:
                list_of_person = floor.get_all_persons_going_down()
            for person in list_of_person:
                waiting_passengers_cost+=person.get_elevator_waiting_time()^2
            cost+=self.w1*waiting_passengers_cost

        if elevator.get_passenger_count>0:
            riding_passengers_cost = 0
            list_of_person = elevator.get_passenger_list()
            for person in list_of_person:
                riding_passengers_cost+=person.get_riding_time()^2
            cost+=self.w2*riding_passengers_cost
        
        if elevator.car_calls_left()>0:
            list_car_calls = elevator.get_car_calls()
            elevator_moving_distance_cost = 0
            if elevator.get_direction() == "UP":
                for i in range(len(list_car_calls)):
                    if i==0:
                        prev_floor = elevator.get_current_floor()
                    else:
                        prev_floor = list_car_calls[i-1]
                    next_floor = list_car_calls[i]
                    elevator_moving_distance_cost+=next_floor-prev_floor
            else:
                for i in range(start=-1,stop=-len(list_car_calls)-1,step=-1):
                    if i==-1:
                        prev_floor = elevator.get_current_floor()
                    else:
                        prev_floor = list_car_calls[i-1]
                    next_floor = list_car_calls[i]
                    elevator_moving_distance_cost+=next_floor-prev_floor
            cost+=self.w3*elevator_moving_distance_cost
        return cost
            




    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()
