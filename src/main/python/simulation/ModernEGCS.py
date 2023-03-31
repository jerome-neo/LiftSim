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
        self.hallcall_priority_arrays = [] #stores complete set of priority arrays
        self.hall_call_priority_evaluation = [] #stores only the first element of each hall call's priority array
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

    def add_hall_call(self,hall_call) -> None:
        """Appends a new hall call to the list of unassigned hall calls.
        Hall calls are represented by a tuple: (source floor of the call, direction of the call)"""
        self.unassigned_hall_calls.append(hall_call)
        priority_array = self.create_call_priority_array(hall_call)
        ls = [hall_call,priority_array]
        ls_1 = (len(self.hallcall_priority_arrays),priority_array[0])
        self.hallcall_priority_arrays.append(ls)
        self.hall_call_priority_evaluation.append(ls_1)


    def handle_person(self, person) -> None:
        """
        Handles a person who wants to use the elevator system.

        Args:
            person (Person): The person who wants to use the elevator system.
        """
        # Put the person in the floor and call the lift
        call_direction = person.get_direction()
        curr_floor = self.floors[person.get_curr_floor() - 1]
        building = curr_floor.get_building()
        if call_direction < 0:
            curr_floor.add_person_going_down(person)
            if not curr_floor.has_call_down():
                curr_floor.set_call_down()
                curr_floor.person_arrived()
                hall_call = HallCall.HallCall(self.env,curr_floor.get_floor_level(),-1)
                self.add_hall_call(hall_call)

        else:
            curr_floor.add_person_going_up(person)
            if not curr_floor.has_call_up():
                curr_floor.set_call_up()
                curr_floor.person_arrived()
                hall_call = HallCall.HallCall(self.env,curr_floor.get_floor_level(),1)
                self.add_hall_call(hall_call)
        
    
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

        for person in waiting_passengers_hallcall:
            waiting_passengers_cost += ((now-person.get_arrival_time()) + floors_til_arrival*6)^2
            riding_passengers_cost += person.get_riding_time()^2 #assume we can load everyone registered under this hallcall
        elevator_moving_distance_cost=(current_elevator_moving_distance - initial_elevator_moving_distance)
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
        return converted_priority_array

    def assign_calls(self) -> None:
        """Assigns hall call to the most suitable elevator based on HCPM method."""
        if len(self.hallcall_priority_arrays)>0:
            while len(self.hall_call_priority_evaluation)>1:
                self.hall_call_priority_evaluation.sort(key=lambda x: x[1][1],reverse=True)
                lowest_cost = self.hall_call_priority_evaluation[-1][1][1]
                prioritised_hall_call_index = self.hall_call_priority_evaluation[0][0]
                current_best_elevator = self.hall_call_priority_evaluation[0][1][0]
                current_cost = self.hall_call_priority_evaluation[0][1][1]
                if self.elevators[current_best_elevator-1].has_more_than_optimum_calls():
                    updated_cost = current_cost - self.hallcall_priority_arrays[prioritised_hall_call_index][1][1]
                    if updated_cost>lowest_cost:
                        next_best_elevator = self.hallcall_priority_arrays[prioritised_hall_call_index][1][0]
                        tup = (prioritised_hall_call_index,(next_best_elevator,updated_cost))
                        self.hall_call_priority_evaluation.append(tup)
                        pass
                self.assign_one_call(prioritised_hall_call_index,current_best_elevator)
                del self.hall_call_priority_evaluation[0]
                del self.hallcall_priority_arrays[prioritised_hall_call_index] 
                
            best_elevator_index = self.hall_call_priority_evaluation[0][1][0]
            self.assign_one_call(0,best_elevator_index)
            del self.hall_call_priority_evaluation[0]
            del self.hallcall_priority_arrays[0] 

    
    def assign_one_call(self,prioritised_hall_call_index,best_elevator_index) -> None:
            """Assign one hall call to the most suitable elevator based on HCPM method, when there is only 1 registered hall call"""
            hall_call = self.hallcall_priority_arrays[prioritised_hall_call_index][0]
            hall_call_floor = hall_call.get_source_floor()
            hall_call_direction = hall_call.get_direction()
            best_elevator = self.elevators[best_elevator_index]
            best_elevator.add_path(hall_call_floor,hall_call_direction)
                

    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                self.assign_calls()
                if elevator.is_busy():
                    pass
                busiest_floor_level = self.building.get_busiest_floor()
                idling_elevators_deserved = busiest_floor_level.get_num_idling_elevators_deserved()
                idling_elevators_sent = busiest_floor_level.get_num_idling_elevators_sent()
                if idling_elevators_deserved>=idling_elevators_sent+1:
                    elevator.travel(busiest_floor_level)
                
