import simpy

class Floor(object):
    """A class representing a floor in a building."""
    def __init__(self, env: simpy.Environment, index: int):
        """
        Initialize the floor with the given index.

        Args:
            env (simpy.Environment): The simulation environment.
            index (int): The index of the floor.
        """
        self.env = env
        self.floor_index = index
        self.call_up = False
        self.call_down = False
        self.call_up_accepted = False
        self.call_down_accepted = False
        self.total_people_arrived = 0
        self.people_arrival_rate = 0
        self.idling_elevators_deserved = 0
        self.idling_elevators_sent = 0
       
    def __str__(self):
        """
        Return a string representation of the floor.

        Returns:
            str: A string representation of the floor.
        """
        return f"Floor {self.floor_index}"

    def has_call_down(self) -> bool:
        """Returns the call_down flag."""
        return self.call_down

    def has_call_up(self) -> bool:
        """Returns the call_up flag"""
        return self.call_up

    def set_call_up(self) -> bool:
        """Set the call_up flag to True."""
        self.call_up = True

    def set_call_down(self) -> None:
        """Set the call_down flag to True."""
        self.call_down = True

    def uncall_up(self) -> None:
        """Set the call_up flag to False."""
        self.call_up = False

    def uncall_down(self) -> None:
        """Set the call_down flag to False."""
        self.call_down = False

    def get_floor_level(self) -> int:
        """
        Return the index of the floor.

        Returns:
            int: The index of the floor.
        """
        return self.floor_index

    # Checking status of calls being attended to by an elevator
    def is_call_down_accepted(self):
        return self.call_down_accepted

    def is_call_up_accepted(self):
        return self.call_up_accepted

    def accept_down_call(self) -> None:
        self.call_down_accepted = True

    def accept_up_call(self) -> None:
        self.call_up_accepted = True

    def unaccept_down_call(self) -> None:
        self.call_down_accepted = False

    def unaccept_up_call(self) -> None:
        self.call_up_accepted = False
    
    def person_arrived(self, building) -> None:
        """
        Updates the count for total people arrived and arrival rate for the floor. Used in ModernEGCS.
        """
        self.total_people_arrived += 1
        self.people_arrival_rate = self.total_people_arrived / self.env.now
        building.update_floor_arrival_rate(self.floor_index-1, self.people_arrival_rate)
        sum_arrival_rates_floors = building.get_sum_arrival_rates_floors()
        building_num_floors = building.get_num_floors()
        self.idling_elevators_deserved = self.people_arrival_rate/sum_arrival_rates_floors*building_num_floors

    def new_idling_elevator_sent(self) -> None:
        """Updates the count of idling elevators sent to this floor"""
        self.idling_elevators_sent += 1
    
    def get_num_idling_elevators_sent(self) -> None:
        """Returns the count of idling elevators sent to this floor"""
        return self.idling_elevators_sent
    
    def get_num_idling_elevators_deserved(self) -> None:
        """Returns the count of idling elevators sent to this floor"""
        return self.idling_elevators_deserved
    
