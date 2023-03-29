import Elevator
import HallCall

class ModernEGCS(object):
    """
    A system for controlling a group of elevators in a building using ModernEGCS algorithm.

    Attributes:
        env (simpy.Environment): The simulation environment.
        floors (list of Floor): The collection of floors in the building.
        elevators (list of Elevator): The collection of elevators within the building system.
        unassigned_hall_calls (list of two-element tuples): The queue of unassigned hall calls
    """
    def __init__(self, env, collection_floors, num_elevators,w1,w2,w3):
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
        self.floors = collection_floors
        self.elevators = [Elevator.Elevator(env, i, self.floors, 1) for i in range(1, num_elevators + 1)]
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

    def add_hall_call(self,hall_call) -> None:
        """Appends a new hall call to the list of unassigned hall calls.
        Hall calls are represented by a tuple: (source floor of the call, direction of the call)"""
        self.unassigned_hall_calls.append(hall_call)

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
            if not curr_floor.has_call_down():
                curr_floor.set_call_down()
                hall_call = HallCall.HallCall(self.env,curr_floor.get_floor_level(),-1)
                self.add_hall_call(hall_call)

        else:
            curr_floor.add_person_going_up(person)
            if not curr_floor.has_call_up():
                curr_floor.set_call_up()
                hall_call = HallCall.HallCall(self.env,curr_floor.get_floor_level(),1)
                self.add_hall_call(hall_call)
            
        
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
                    if person_to_add not in riding_passengers_list:
                        riding_passengers_cost+=person_to_add.get_riding_time()^2
                        riding_passengers_count+=1
                        person_dest = person_to_add.get_dest_floor()
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
        elevator_curr_floor = elevator.get_current_floor()
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
            cost1_car_calls.append(person_source_floor)
        if person_dest_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
            cost1_car_calls.append(person_dest_floor)
        cost1_car_calls.sort()

        current_elevator_moving_distance=abs(cost1_car_calls[0]-cost1_car_calls[-1])
        additional_elevator_moving_distance_cost=self.w3*current_elevator_moving_distance - elevator_moving_distance_cost1

        total_cost2 = waiting_passengers_cost1 + additional_waiting_passengers_cost + riding_passengers_cost1 + additional_riding_passengers_cost + elevator_moving_distance1 + additional_elevator_moving_distance
        return total_cost2
        
    
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
        elevator_capacity = elevator.get_capacity()
        elevator_passengers_count = elevator.get_passenger_count()
        elevator_passengers_list = elevator.get_passenger_list()
        elevator_carcalls_list = elevator.get_car_calls()

        hall_call_floor = hall_call.get_source_floor()
        hall_call_direction = hall_call.get_direction()
        now = self.env.now

        waiting_passengers_cost = 0
        riding_passengers_cost = 0
        elevator_moving_distance_cost = 0

        if elevator_direction == hall_call_direction:
            if hall_call_direction == "UP":
                waiting_passengers_hallcall = self.floors[hall_call_floor-1].get_all_persons_going_up()
                waiting_passengers_elevator_curr_floor = self.floors[elevator_curr_floor-1].get_all_persons_going_up()
            else:
                waiting_passengers_hallcall = self.floors[hall_call_floor-1].get_all_persons_going_down()
                waiting_passengers_elevator_curr_floor = self.floors[elevator_curr_floor-1].get_all_persons_going_down()
            
            if not elevator.is_moving():
                index = 0
                while elevator_passengers_count<elevator_capacity() and index<len(waiting_passengers_elevator_curr_floor):
                    person_to_add = waiting_passengers_elevator_curr_floor[index]
                    if person_to_add not in elevator_passengers_list:
                        person_dest = person_to_add.get_dest_floor()
                        elevator_passengers_count+=1
                        if person_dest not in elevator_carcalls_list:
                            elevator_carcalls_list.append(person_dest)
                            elevator_carcalls_list.sort()
                    index+=1
            
            floors_til_arrival = 0
            for floor in elevator_carcalls_list:
                if floor<hall_call_floor:
                    floors_til_arrival+=1
                else:
                    break
            if hall_call_direction == "DOWN":
                floors_til_arrival = len(elevator_carcalls_list)-floors_til_arrival-1

            for person in waiting_passengers_hallcall:
                waiting_passengers_cost += ((now-person.get_arrival_time()) + floors_til_arrival*3)^2
                riding_passengers_cost += person.get_riding_time()^2 #assume we can load everyone registered under this hallcall
            
            first_car_call_in_list = elevator_carcalls_list[0]
            last_car_call_in_list = elevator_carcalls_list[-1]
            initial_elevator_moving_distance = abs(last_car_call_in_list - first_car_call_in_list)
            
            if hall_call_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
                elevator_carcalls_list.append(hall_call_floor)
            if hall_call_floor not in range(first_car_call_in_list, last_car_call_in_list+1):
                elevator_carcalls_list.append(hall_call_floor)
            elevator_carcalls_list.sort()

            current_elevator_moving_distance=abs(elevator_carcalls_list[0]-elevator_carcalls_list[-1])
            elevator_moving_distance_cost=(current_elevator_moving_distance - initial_elevator_moving_distance)
            
            cost2_minus_cost1 = self.w1*waiting_passengers_cost + self.w2*riding_passengers_cost + elevator_moving_distance_cost
            return cost2_minus_cost1
    
    def create_call_priority_array(self,person) -> list:
        """
        Creates priority array for each hall call, which will be evaluated for elevator allocation by the HCPM method.

        Args:
            person: an object of Person class representing the person whose ha
        """


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

    def update_status(self) -> None:
        """Updates the elevators to be idle when they have no path."""
        for elevator in self.elevators_down + self.elevators_up:
            if not elevator.has_path() and elevator.is_busy():
                elevator.set_idle()
