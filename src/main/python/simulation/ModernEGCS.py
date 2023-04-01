import Elevator
import HallCall
import Building


class ModernEGCS(object):
    """
    A system for controlling a group of elevators in a building using ModernEGCS algorithm.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators (list of Elevator): The collection of elevators within the building system.
        unassigned_hall_calls (list of two-element tuples): The queue of unassigned hall calls
    """
    def __init__(self, env, building, collection_floors, num_elevators,w1,w2,w3):
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

        """
        self.env = env
        self.building = building
        self.floors = collection_floors
        self.elevators = [Elevator.Elevator(env, i, self.floors, 1,num_elevators) for i in range(1, num_elevators + 1)]
        self.unassigned_hall_calls = []
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
    

    def to_dict(self) -> dict:
        """Converts elevator group information into a dictionary with time stamp."""
        return {self.env.now: [{index+1: elevator.to_dict()} for index, elevator
                                in enumerate(self.elevators)]}

    def get_algo_type(self):
        """Returns type of elevator algorithm implemented"""
        return "ModernEGCS"

    def add_hall_call(self,hall_call) -> None:
        """Appends a new HallCall to the list of unassigned hall calls."""
        self.unassigned_hall_calls.append(hall_call)
        priority_array = self.create_call_priority_array(hall_call)
        hall_call.set_priority_array(priority_array)
        
    
    def calculate_cost2_minus_cost1_efficient(self,hall_call,elevator):
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
        elevator_carcalls_list = elevator.get_car_calls()

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

        if len(elevator_carcalls_list)>0:
            first_car_call_in_list = elevator_carcalls_list[0]
            last_car_call_in_list = elevator_carcalls_list[-1]
            initial_elevator_moving_distance = abs(last_car_call_in_list - first_car_call_in_list)
        
        
            if elevator_direction is not None and elevator_direction == hall_call_direction:  
                for floor in elevator_carcalls_list:
                    if floor<hall_call_floor:
                        floors_til_arrival+=1
                    else:
                        break

                if hall_call_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
                    elevator_carcalls_list.append(hall_call_floor)
                elevator_carcalls_list.sort()
                current_elevator_moving_distance=elevator_carcalls_list[0]-elevator_carcalls_list[-1]
                
            else: #elevator currently either moving in an opposite direction to the hall call or have no direction (currently idle)
                if elevator_direction == "UP":
                    topmost_level = self.floors[-1].get_floor_level()
                    floors_til_arrival = (topmost_level - elevator_carcalls_list[0]) + (elevator_carcalls_list[0]-elevator_curr_floor) + (topmost_level-hall_call_floor) #assume that elevator will operate until top-most level until it switches direction
                    current_elevator_moving_distance = (topmost_level - elevator_carcalls_list[0]) + (topmost_level-hall_call_floor)
                elif elevator_direction == "DOWN":
                    bottommost_level = self.floors[0].get_floor_level()
                    floors_til_arrival = (elevator_carcalls_list[-1]-bottommost_level) + (elevator_curr_floor-elevator_carcalls_list[-1]) + (hall_call_floor-bottommost_level) #assume that elevator will operate until bottom-most level until it switches direction
                    current_elevator_moving_distance = (elevator_carcalls_list[-1] - bottommost_level) + (hall_call_floor-bottommost_level)
                else:
                    current_elevator_moving_distance = abs(elevator_curr_floor - hall_call_floor)
            elevator_moving_distance_cost=(current_elevator_moving_distance - initial_elevator_moving_distance)

        for person in waiting_passengers_hallcall:
            waiting_passengers_cost += ((now-person.get_arrival_time()) + floors_til_arrival*6)**2
            riding_passengers_cost += person.get_riding_time(elevator)**2 #assume we can load everyone registered under this hallcall
        cost2_minus_cost1 = self.w1*waiting_passengers_cost + self.w2*riding_passengers_cost + self.w3*elevator_moving_distance_cost
        return cost2_minus_cost1
        
    
    def create_call_priority_array(self,hall_call) -> list:
        """
        Creates priority array for each hall call, which will be evaluated for elevator allocation by the HCPM method.

        Args:
            hall_call: an object of HallCall class representing the elevator hall call which priority we are evaluating 
        """
        priority_array = []
        elevators = self.elevators
        for elevator in elevators:
            value = self.calculate_cost2_minus_cost1_efficient(hall_call,elevator)
            elevator_index = elevator.get_index()
            tup = (elevator_index,value)
            priority_array.append(tup)
        priority_array.sort(key= lambda x: x[1])

        converted_priority_array = []
        for i in range(len(priority_array)-1):
            value_element = priority_array[i+1][1]-priority_array[i][1]
            index = priority_array[i][0]
            tup = (index,value_element)
            converted_priority_array.append(tup)
        last_elevator_index = priority_array[-1][0]
        tup = (last_elevator_index,-1)
        converted_priority_array.append(tup)
        return converted_priority_array
    
    def assign_calls(self)-> None:
        """Assigns hall call to the most suitable elevator based on HCPM method."""
        print(f"{self.unassigned_hall_calls} (function start)")
        if len(self.unassigned_hall_calls)>0:
            while len(self.unassigned_hall_calls)>1:
                self.unassigned_hall_calls.sort(key=lambda x: x.get_first_priority_value(),reverse=True)
                lowest_value_hall_call = self.unassigned_hall_calls.pop(-1)
                lowest_cost = lowest_value_hall_call.get_first_priority_value()

                prioritised_hall_call = self.unassigned_hall_calls.pop(0)
                current_best_elevator_index = prioritised_hall_call.get_current_best_elevator()
                current_best_elevator = self.elevators[current_best_elevator_index-1]
                current_cost = prioritised_hall_call.get_first_priority_value()

                if current_best_elevator.has_more_than_optimum_calls() and len(self.unassigned_hall_calls)>1 and prioritised_hall_call.get_priority_array_length()>0:
                    decrease_in_cost = prioritised_hall_call.get_second_priority_value()
                    if decrease_in_cost>-1:
                        updated_cost = current_cost - decrease_in_cost
                        if updated_cost>lowest_cost:
                            prioritised_hall_call.remove_frontmost_array_pair()
                            pass
                self.assign_one_call(prioritised_hall_call,current_best_elevator)
                self.unassigned_hall_calls = self.unassigned_hall_calls[1:]

            if len(self.unassigned_hall_calls) == 1:
                last_hall_call = self.unassigned_hall_calls[0]
                best_elevator_index = last_hall_call.get_current_best_elevator()
                best_elevator = self.elevators[best_elevator_index-1]
                self.assign_one_call(last_hall_call,best_elevator)
                self.unassigned_hall_calls = []
            print(f"{self.unassigned_hall_calls} (function end)")
            
    
    def assign_one_call(self,hall_call: HallCall, elevator: Elevator) -> None:
            """Assign one hall call to the most suitable elevator based on HCPM method, when there is only 1 registered hall call"""
            hall_call_floor = hall_call.get_source_floor()
            hall_call_direction = hall_call.get_direction()
            elevator.set_busy()
            elevator.add_path(hall_call_floor,hall_call_direction)
            floor = self.floors[hall_call_floor-1]
            if hall_call_direction == "UP":
                floor.accept_up_call()
            else:
                floor.accept_down_call()
            print(f"Hall call from {hall_call_floor} going {hall_call_direction} is assigned to {elevator.index}")
            
                
    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path.
        Reassigns hall calls and moves idle elevators to busier floors at ever hour"""
        for elevator in self.elevators:
            if elevator.num_active_calls==0 and elevator.is_busy():
                if self.env.now % 3600 == 0:
                    self.assign_calls()
                    if elevator.is_busy():
                        pass
                    busiest_floor_level = self.building.get_busiest_floor()
                    busiest_floor = self.floors[busiest_floor_level-1]
                    idling_elevators_deserved = busiest_floor.get_num_idling_elevators_deserved()
                    idling_elevators_sent = busiest_floor.get_num_idling_elevators_sent()
                    if idling_elevators_deserved>=idling_elevators_sent+1:
                        busiest_floor.new_idling_elevator_sent()
                        elevator.travel(busiest_floor_level)
                        elevator.unset_direction()
                elevator.set_idle()
    
    def is_all_idle(self) -> bool:
        """Returns True if all the elevators are idle"""
        return all(map(lambda x: x.is_busy(), self.elevators))

    def print_system_status(self) -> str:
        """Returns a string representation number of active elevators."""
        num_active_up = len(list(filter(lambda x: x.is_busy() and x.direction == "UP", self.elevators)))
        num_active_down = len(list(filter(lambda x: x.is_busy() and x.direction == "DOWN", self.elevators)))
        return f"Elevator system has {num_active_up} UP and {num_active_down} DOWN elevator(s) ACTIVE"
    
