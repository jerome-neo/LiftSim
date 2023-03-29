import random
import LiftRandoms
import Elevator

class Person(object):
    """A person in the building.

    Attributes:
        id (int): The unique identifier of the person.
        env (simpy.Environment): The simulation environment.
        curr_floor (int): The floor where the person is currently located.
        destination_floor (int): The floor where the person wants to go.
        arrival_time (float): The time when the person arrives in the building.
        end_time (float): The time when the person completes their trip.
        has_reached_floor (bool): Whether the person has reached their destination floor.

    """
    def __init__(self, env, index, building):
        """Initializes a new Person object.

        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The unique identifier of the person.
            building (Building): The building where the person is located.

        """
        self.id = index
        self.env = env
        self.arrival_time = env.now #arrival time of person's request
        self.elevator_arrival_time = None #time taken for the elevator to reach the person, i.e. for the person's hall call to be answered
        self.end_time = None

        self.entered_elevator = False
        self.has_reached_floor = False
        random_variable_generator=LiftRandoms.LiftRandoms()
        self.curr_floor=0
        self.destination_floor=0

        while self.curr_floor==self.destination_floor:
            self.curr_floor,self.destination_floor=random_variable_generator.generate_source_dest(self.arrival_time)
        
        
        print(f"Source: {self.curr_floor}, Dest: {self.destination_floor}")
        print(f"Arrival time: {self.arrival_time}")

    def __str__(self):
        """Returns a string representation of the Person object."""
        return f"Person {self.id} starting at {self.curr_floor} and going to {self.destination_floor}:"

    def calls_elevator(self) -> None:
        """
        Simulates a person calling an elevator.

        This method waits for one unit of time to simulate the time taken for a person to call an elevator.
        """
        yield self.env.timeout(1)

    def has_reached_destination(self, elevator) -> bool:
        """
        Checks if the person has reached their destination floor.

        Args:
            elevator (Elevator): The elevator that the person is in.

        Returns:
            bool: True if the person has reached their destination floor, False otherwise.

        """
        return elevator.get_current_floor() == self.destination_floor

    def complete_trip(self) -> None:
        """
        Marks the person's trip as complete.

        This method updates the end_time and has_reached_floor attributes to indicate that the person
        has completed their trip.

        """
        self.end_time = self.env.now
        self.has_reached_floor = True

    def has_completed_trip(self) -> bool:
        """
        Checks if the person has completed their trip.

        Returns:
            bool: True if the person has completed their trip, False otherwise.

        """
        return self.has_reached_floor

    def get_wait_time(self) -> float:
        """
        Returns the time taken for the person to complete their trip.

        Returns:
            float: The time taken for the person to complete their trip.

        """
        time_taken_to_complete = self.end_time - self.arrival_time
        return time_taken_to_complete

    def get_curr_floor(self) -> int:
        """
        Returns the current floor where the person is located.

        Returns:
            int: The current floor where the person is located.

        """
        return self.curr_floor

    def get_dest_floor(self) -> int:
        """
        Returns the destination floor where the person wants to go.

        Returns:
            int: The destination floor where the person wants to go.

        """
        return self.destination_floor

    def get_direction(self) -> int:
        """
        Returns the direction that the person wants to go.

        Returns:
            int: -1 if the person wants to go down, 1 if the person wants to go up.

        """
        return -1 if self.curr_floor > self.destination_floor else 1

    def get_assigned_elevator(self)-> Elevator:
        """
        Returns the object of the assigned Elevator
        """
        return self.assigned_elevator

    def get_elevator_arrival_time(self)-> float:
        """
        Returns the person's assigned elevator's arrival time
        """
        return self.elevator_arrival_time
        
    def get_riding_time(self)-> float:
        """
        Returns the estimated riding time of the person, which is time from the moment the person enters the assigned
        to the moment the person leaves the elevator, i.e. when the elevator has reached the person's destination.
        Used in ModernEGCS cost calculation.

        Returns:
            float: The length of time spent by the person in the elevator
        """
        if self.get_elevator_arrival_time() is None:
            elevator_arrival_to_now = 0
        else:
            elevator_arrival_to_now = self.env.now-self.get_elevator_arrival_time()
        assigned_elevator = self.get_assigned_elevator()
        elevator_remaining_car_calls_count = len(elevator_assigned.get_car_calls())
        elevator_current_floor = assigned_elevator.get_current_floor()
        person_destination_floor = self.get_dest_floor()
        estimated_remaining_travel_time = abs(person_destination_floor-elevator_current_floor)+3*(elevator_remaining_car_calls_count-1)
        time_taken_to_ride = elevator_arrival_to_now + estimated_remaining_travel_time
        return time_taken_to_ride
    
    def get_elevator_waiting_time(self)->float:
        """
        Returns the length of time spent waiting for the elevator to come and service the person's call.

        Returns:
            float: THe length of time spent waiting for the elevator by the person
        """
        time_taken_for_elevator_arrival = self.elevator_arrival_time - self.arrival_time
        return time_taken_for_elevator_arrival
    
    def succeeds_entering_elevator(self)->None:
        """Updates the person's status of success regarding entering the elevator and updates elevator arrival time"""
        self.entered_elevator = True
        self.elevator_arrival_time = self.env.now
    
    def is_in_elevator(self)->bool:
        """
        Returns whether or not person is inside an elevator

        Returns:
            bool: The person's status of being inside an elevator or not
        """
        return self.entered_elevator

    
    def elevator_arrived(self)->None:
        """
        Updates elevator arrival times
        """
        self.elevator_arrival_time = self.env.now
