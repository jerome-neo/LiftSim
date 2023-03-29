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
        
    def calculate_cost1(self,elevator) -> tuple:
        """
        Cost1 = w1*sigma i: waiting passengers(WTi^2+RWTi^2) + w2* sigma i: riding passengers(RTi^2) + w3*PC
        Calculates Cost1 in HCPM algorithm and returns its value and components used in calculate_cost2 function
        
        Waiting Passengers = Passengers currently at the floor where elevator is, who will enter at this floor
        Riding Passengers = Passengers that are already inside the elevator, including those who alight at this floor

        Args:
            Elevator: An Elevator object, for which cost1 is being calculated

        Returns:
            tuple: (total_cost1, waiting_passengers_cost, riding_passengers_cost, elevator_moving_distance_cost, list_car_calls)
        """
        total_cost1 = 0
        waiting_passengers_cost = 0
        riding_passengers_cost = 0
        elevator_moving_distance_cost = 0
        floor = elevator.get_current_floor_object()
        if elevator.get_direction() == "UP":
            waiting_passengers_list = floor.get_all_persons_going_up()
        else:
            waiting_passengers_list = floor.get_all_persons_going_down()
        riding_passengers_list = elevator.get_passenger_list()
        list_car_calls = elevator.get_car_calls()

        if not elevator.is_moving():
            for person in waiting_passengers_list:
                waiting_passengers_cost+=person.get_elevator_waiting_time()^2

        if elevator.get_passenger_count()>0:
            for person in riding_passengers_list:    
                riding_passengers_cost+=person.get_riding_time()^2
                waiting_passengers_cost+=person.get_elevator_waiting_time()^2
            riding_passengers_count = len(riding_passengers_list)
            if not elevator.is_moving():
                index = 0
                while riding_passengers_count<elevator.get_capacity():
                    person_to_add = waiting_passengers_list[index]
                    if person_to_add not in riding passengers_list:
                        riding_passengers_cost+=person.get_riding_time()^2
                        riding_passengers_count+=1
                        person_dest = person.get_dest_floor()
                        if person_dest not in list_car_calls:
                            list_car_calls.append(person_dest)
                            list_car_calls.sort()
                    index+=1
        
        if elevator.car_calls_left()>0:
            elevator_moving_distance_cost+=abs(list_car_calls[0]-list_car_calls[-1])

        total_cost1 = self.w1*waiting_passengers_cost + self.w2*riding_passengers_cost + self.w3*elevator_moving_distance_cost
            
        return total_cost1,waiting_passengers_cost,riding_passengers_cost,elevator_moving_distance_cost,list_car_calls

    def calculate_cost2(self,person,elevator,waiting_passengers_cost1,riding_passengers_cost1,elevator_moving_distance_cost1,cost1_car_calls)-> float:
        """
        Cost2 = w1*sigma i: waiting passengers(WTi^2+RWTi^2) + w2* sigma i: riding passengers(RTi^2) + w3*PC where person's hall call is considered added to the elevator's path
        Calculates cost2 in HCPM algorithm and returns its value
        
        Waiting Passengers = Passengers currently at the floor where elevator is, who will enter at this floor
        Riding Passengers = Passengers that are already inside the elevator, including those who alight at this floor

        Args:
            person: A Person object, representing the hall call which cost we are calculating
            elevator: An Elevator object, for which cost1 is being calculated
            waiting_passengers_cost1: Float which is output from calculate_cost1, represents the cost incurred by waiting passengers serviced by the elevator
            riding_passengers_cost1: Float which is output from calculate_cost1, represents the cost incurred by riding passengers serviced by the elevator
            elevator_moving_distance1: Float which is output from calculate_cost1, represents the cost incurred by elevator's total moving distance based on current car calls

        Returns:
            float: total_cost2
        """
        elevant_curr_floor = elevator.get_current_floor()
        person_dest_floor = person.get_dest_floor()
        person_source_floor = person.get_curr_floor()
        to_wait_for_elevator_arrival = 0
        for floor in cost1_car_calls:
            if floor<person_source_floor:
                to_wait_for_elevator_arrival+=1
            else:
                break
            
        person_arrival_to_now = self.env.now - self.person.get_person_arrival_time()
        estimated_remaining_waiting_time = abs(person_source_floor-elevator_curr_floor)+to_wait_for_elevator_arrival*3
        person_waiting_time = person_arrival_to_now + estimated_remaining_waiting_time #person's estimated waiting time if their hall call is assigned to this elevator
        additional_waiting_passengers_cost = self.w1*person_waiting_time^2
        
        person_riding_time = person.get_riding_time() #person's estimated riding time if their hall call is assigned to this elevator
        additional_riding_passengers_cost = self.w2*person_riding_time^2

        first_car_call_in_list = cost1_car_calls[0]
        last_car_call_in_list = cost1_car_calls[-1]
        
        if person_source_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
            cost1_car_calls.append(person_source_floor):
        if person_dest_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
            cost1_car_calls.append(person_dest_floor)
        cost1_car_calls.sort()

        current_elevator_moving_distance=abs(cost1_car_calls[0]-cost1_car_calls[-1])
        additional_elevator_moving_distance_cost=self.w3*current_elevator_moving_distance - elevator_moving_distance_cost1

        total_cost2 = waiting_passengers_cost1 + additional_waiting_passengers_cost + riding_passengers_cost1 + additional_riding_passengers_cost + elevator_moving_distance1 + additional_elevator_moving_distance
        return total_cost2
        



































        
        

    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()
