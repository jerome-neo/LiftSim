import src.main.python.simulation.Elevator as Elevator
import src.main.python.simulation.HallCall as HallCall
import src.main.python.simulation.Building as Building


class ModernEGCS(object):
    """
    A system for controlling a group of elevators in a building using ModernEGCS algorithm.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators (list of Elevator): The collection of elevators within the building system.
        unassigned_hall_calls (list of two-element tuples): The queue of unassigned hall calls
    """
    def __init__(self, env, building, collection_floors, num_elevators, w1, w2, w3):
        """
        Initializes a ModernEGCS.

        Args:
            env (simpy.Environment): The simulation environment.
            building (Building.Building): The Building object where simulation takes place.
            collection_floors (list of Floor): The collection of floors in the building.
            num_elevators (int): The number of elevators in the system.
            w1: w1 for cost calculation in HCPM
            w2: w2 for cost calculation in HCPM
            w3: w3 for cost calculation in HCPM
            reassigning (bool): True if reassign_hall_calls is running, False otherwise.
            calls_backlog (list): List of HallCall objects with empty priority array \
            due to unavailability of elevators serving the direction they want to go 
            backlog_time_start (int): Time at which the earliest backlog is added
        """
        self.env = env
        self.building = building
        self.floors = collection_floors
        self.elevators = [Elevator.Elevator(env, i, self.floors, 1, num_elevators) for i in range(1, num_elevators + 1)]
        self.unassigned_hall_calls = []
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.reassigning = False
        self.calls_backlog = []
        self.backlog_time_start = None

    def __str__(self):
        """
        Returns a string representation of the ElevatorSystem.

        Returns:
            str: A string representation of the ElevatorSystem.

        """
        return f"ModernEGCS with {len(self.elevators)} elevators."

    def to_dict(self) -> dict:
        """Converts elevator group information into a dictionary with time stamp."""
        return {self.env.now: [{index+1: elevator.to_dict()} for index, elevator
                                in enumerate(self.elevators)]}

    def get_algo_type(self):
        """Returns type of elevator algorithm implemented"""
        return "ModernEGCS"

    def add_hall_call(self, hall_call) -> None:
        """Appends a new HallCall to the list of unassigned hall calls."""
        self.unassigned_hall_calls.append(hall_call)
        priority_array = self.create_call_priority_array(hall_call)
        hall_call.set_priority_array(priority_array)

    def calculate_cost2_minus_cost1_efficient(self, hall_call, elevator):
        """
        Cost1 = w1*sigma i: waiting passengers(WTi^2+RWTi^2) + w2* sigma i: riding passengers(RTi^2) + w3*PC
        Cost2 = w1*sigma i: waiting passengers(WTi^2+RWTi^2) + w2* sigma i: riding passengers(RTi^2) + w3*PC where hall call is considered added to the elevator's path
        Calculates Cost2-Cost1 which is input to pstr_array used to determine priority
        
        Waiting Passengers = Passengers currently at the floor where elevator is, who will enter at this floor
        Riding Passengers = Passengers that are already inside the elevator, including those who alight at this floor

        Args:
            hall_call: A HallCall object 
            Elevator: An Elevator object, for which cost2-cost1 is being calculated

        Returns:
            value: cost2_minus_cost1
        """
        elevator_curr_floor = elevator.get_current_floor()
        elevator_direction = elevator.get_direction()
        elevator_path = elevator.get_path().copy()

        hall_call_floor = hall_call.get_source_floor()
        hall_call_direction = hall_call.get_direction()
        now = self.env.now

        waiting_passengers_cost = 0
        riding_passengers_cost = 0
        elevator_moving_distance_cost = 0

        if hall_call_direction == "UP":
            waiting_passengers_hallcall = self.floors[hall_call_floor-1].get_all_persons_going_up()
        else:
            waiting_passengers_hallcall = self.floors[hall_call_floor-1].get_all_persons_going_down()
        floors_til_arrival = 0

        if len(elevator_path) > 0:
            first_in_list = elevator_path[0]
            last_in_list = elevator_path[-1]
            initial_elevator_moving_distance = abs(last_in_list - first_in_list)

            if elevator_direction == hall_call_direction:
                for floor in elevator_path:
                    if floor < hall_call_floor and elevator_direction == "UP":
                        floors_til_arrival += 1
                    elif floor > hall_call_floor and elevator_direction == "DOWN":
                        floors_til_arrival+=1
                    else:
                        break

                if hall_call_floor not in range(first_in_list, last_in_list+1):
                    elevator_path.append(hall_call_floor)
                elevator_path.sort()
                current_elevator_moving_distance=abs(elevator_path[0]-elevator_path[-1])
                
            else:  # elevator currently either moving in an opposite direction to the hall call
                # or have no direction (currently idle)
                if elevator_direction == "NIL":
                    current_elevator_moving_distance = abs(elevator_curr_floor - hall_call_floor)
                else:
                    return -1
            elevator_moving_distance_cost = (current_elevator_moving_distance - initial_elevator_moving_distance)

        for person in waiting_passengers_hallcall:
            waiting_passengers_cost += ((now-person.get_arrival_time()) + floors_til_arrival*6)**2
            riding_passengers_cost += person.get_riding_time(elevator)**2
            # assume we can load everyone registered under this HallCall
        cost2_minus_cost1 = \
            self.w1 * waiting_passengers_cost \
            + self.w2 * riding_passengers_cost \
            + self.w3 * elevator_moving_distance_cost
        return cost2_minus_cost1

    def create_call_priority_array(self, hall_call) -> list:
        """
        Creates priority array for each hall call, which will be evaluated for elevator allocation by the HCPM method.

        Args:
            hall_call: an object of HallCall class representing the elevator hall call which priority we are evaluating 
        """
        priority_array = []
        elevators = self.elevators
        for elevator in elevators:
            value = self.calculate_cost2_minus_cost1_efficient(hall_call, elevator)
            if value == -1:
                continue
            elevator_index = elevator.get_index()
            tup = (elevator_index, value)
            priority_array.append(tup)
        priority_array.sort(key=lambda x: x[1])
        converted_priority_array = []
        for i in range(len(priority_array)-1):
            value_element = priority_array[i+1][1]-priority_array[i][1]
            index = priority_array[i][0]
            tup = (index, value_element)
            converted_priority_array.append(tup)
        if len(priority_array) > 0:
            last_elevator_index = priority_array[-1][0]
            tup = (last_elevator_index, -1)
            converted_priority_array.append(tup)
        return converted_priority_array
    
    def assign_calls(self) -> None:
        """Assigns hall call to the most suitable elevator based on HCPM method."""
        if self.backlog_time_start is not None and self.env.now - self.backlog_time_start >= 15:
            self.unassigned_hall_calls.extend(self.calls_backlog)
            self.backlog_time_start = None
            self.calls_backlog = []
        if len(self.unassigned_hall_calls) > 0:
            while len(self.unassigned_hall_calls) > 1:
                self.unassigned_hall_calls.sort(key=lambda x: x.get_first_priority_value(), reverse=True)
                prioritised_hall_call = self.unassigned_hall_calls.pop(0)
                priority_array = prioritised_hall_call.get_priority_array()
                if len(priority_array) == 0:
                    new_array = self.create_call_priority_array(prioritised_hall_call)
                    if len(new_array) > 0:
                        prioritised_hall_call.set_priority_array(new_array)
                    else:
                        self.calls_backlog.append(prioritised_hall_call)
                        if self.backlog_time_start is None:
                            self.backlog_time_start = self.env.now
                        continue
                current_best_elevator_index = prioritised_hall_call.get_current_best_elevator()
                current_best_elevator = self.elevators[current_best_elevator_index-1]
                source_floor = prioritised_hall_call.get_source_floor()

                #if (current_best_elevator.is_busy()) and prioritised_hall_call.get_priority_array_length() > 0:
                if (current_best_elevator.has_more_than_optimum_calls() and self.is_there_idle()) \
                or not current_best_elevator.floor_fits_path(source_floor):
                    
                    if prioritised_hall_call.get_priority_array_length() > 1 :
                        prioritised_hall_call.remove_frontmost_array_pair()
                        self.unassigned_hall_calls.append(prioritised_hall_call)
                        continue
                    else:
                        self.calls_backlog.append(prioritised_hall_call)
                        if self.backlog_time_start is None:
                            self.backlog_time_start = self.env.now
                        continue
                else:
                    self.assign_one_call(prioritised_hall_call, current_best_elevator)
                
            if len(self.unassigned_hall_calls) == 1:
                last_hall_call = self.unassigned_hall_calls.pop(0)
                self.unassigned_hall_calls = [] #reset list
                priority_array = last_hall_call.get_priority_array()
                if len(priority_array) > 0:
                    best_elevator_index = last_hall_call.get_current_best_elevator()
                    best_elevator = self.elevators[best_elevator_index-1]
                    source_floor = last_hall_call.get_source_floor()
                    while (self.is_there_idle() and best_elevator.has_more_than_optimum_calls()) \
                    or not best_elevator.floor_fits_path(source_floor):
                        if last_hall_call.get_priority_array_length() > 1:
                            last_hall_call.remove_frontmost_array_pair()
                            best_elevator_index = last_hall_call.get_current_best_elevator()
                            best_elevator = self.elevators[best_elevator_index-1]
                        else:
                            self.calls_backlog.append(last_hall_call)
                            if self.backlog_time_start is None:
                                self.backlog_time_start = self.env.now 
                            break
                    if best_elevator.floor_fits_path(source_floor):
                        self.assign_one_call(last_hall_call, best_elevator)
                else:
                    new_array = self.create_call_priority_array(last_hall_call)
                    last_hall_call.set_priority_array(new_array)
                    self.unassigned_hall_calls.append(last_hall_call)
                    

    def assign_one_call(self, hall_call: HallCall, elevator: Elevator) -> None:
        """Assign one hall call to the most suitable elevator based on HCPM method,
        when there is only 1 registered hall call.
        Args:
            hall_call(HallCall): HallCall object which is being assigned
            elevator(Elevator): Elevator to which HallCall is assigned"""
        hall_call_floor = hall_call.get_source_floor()
        hall_call_direction = hall_call.get_direction()
        
        call_successfully_assigned = elevator.add_hall_call(hall_call_floor, hall_call_direction)
        if call_successfully_assigned:
            elevator.set_busy()
            floor = self.floors[hall_call_floor-1]
            if hall_call_direction == "UP":
                floor.accept_up_call()
            else:
                floor.accept_down_call()
            print(f"Hall call from {hall_call_floor} going {hall_call_direction} is assigned to {elevator.index}")
        else:
            self.calls_backlog.append(hall_call)
            if self.backlog_time_start is None:
                self.backlog_time_start = self.env.now
            print(f"Hall call from {hall_call_floor} going {hall_call_direction} COULD NOT be assigned to {elevator.index} so it is reevaluated")


    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path.
        Reassigns hall calls and moves idle elevators to busier floors at every hour"""
        for elevator in self.elevators:
            if len(elevator.path) == 0 and elevator.is_busy():
                elevator.set_idle("ModernEGCS")

        if self.env.now % 300 == 0:
            self.reassign_hall_calls()
            for elevator in self.elevators:
                if elevator.is_busy():
                    continue
                busiest_floor_level = self.building.get_busiest_floor()
                busiest_floor = self.floors[busiest_floor_level-1]
                idling_elevators_deserved = busiest_floor.get_num_idling_elevators_deserved()
                idling_elevators_sent = busiest_floor.get_num_idling_elevators_sent()
                if idling_elevators_deserved >= idling_elevators_sent + 1:
                    busiest_floor.new_idling_elevator_sent()
                    elevator.add_path(busiest_floor_level)
                    elevator.unset_direction()
                
    
    def recalculate_priority_array(self)-> None:
        """Recalculates cost and reconstructs priority array to be used for call reassignment in update_status()"""

    
    def is_all_idle(self) -> bool:
        """Returns True if all the elevators are idle"""
        return all(map(lambda x: x.is_busy(), self.elevators))

    def print_system_status(self) -> str:
        """Returns a string representation number of active elevators."""
        num_active_up = len(list(filter(lambda x: x.is_busy() and x.direction == "UP", self.elevators)))
        num_active_down = len(list(filter(lambda x: x.is_busy() and x.direction == "DOWN", self.elevators)))
        return f"Elevator system has {num_active_up} UP and {num_active_down} DOWN elevator(s) ACTIVE"
    
    def is_there_idle(self) -> bool:
        """Returns True if there are any idle elevators"""
        return any(map(lambda x: x.is_busy(), self.elevators))
    
    def reassign_hall_calls(self) -> None:
        """Recalculates cost and reconstructs priority array for un-served calls, including those that have been
        allocated to elevators."""
        self.reassigning = True
        unserved_calls = []
        for elevator in self.elevators:
            if elevator.is_busy() and len(elevator.hall_calls) > 0:
                elevator_direction = elevator.get_direction()
                direction_num = -1 if elevator_direction == "DOWN" else 1
                floor_currently_served = elevator.get_path()[0] if elevator_direction == "UP" else elevator.get_path()[-1]
                frontmost_hall_call = elevator.hall_calls[0] if elevator_direction == "UP" else elevator.hall_calls[-1]
                if floor_currently_served == frontmost_hall_call and len(elevator.hall_calls) > 1:
                    current_elevator_unserved = elevator.hall_calls[1:]
                elif floor_currently_served != frontmost_hall_call and len(elevator.hall_calls) > 1:
                    current_elevator_unserved = elevator.hall_calls
                else:
                    continue
                for floor in current_elevator_unserved:
                    if floor in elevator.get_path() and floor not in elevator.get_car_calls():
                        elevator.path.remove(floor)
                    hall_call = HallCall.HallCall(self.env, floor, direction_num)
                    unserved_calls.append(hall_call)
        
        to_recalculate = self.unassigned_hall_calls + unserved_calls
        self.unassigned_hall_calls = []
        for call in to_recalculate:
            self.add_hall_call(call)
        self.assign_calls()
        self.reassigning = False
        


