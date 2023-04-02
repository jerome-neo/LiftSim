import simpy

class HallCall(object):
    """A hall call registered to ModernEGCS elevator system.

    Attributes:
        env (simpy.Environment):
        source_floor (int): floor level where elevator button is pressed
        direction (str): direction of elevator call -> UP or DOWN
        registered_time (float): time when call is registered
    """

    def __init__(self, env, source_floor, direction):
        """Initializes a new HallCall object.

        Args:
            source_floor(int): floor level where elevator button is pressed
            direction(int): direction of elevator call -> -1 is down, 1 is up

        """
        self.env = env
        self.source_floor = source_floor
        if direction == 1:
            self.direction = "UP"
        elif direction == -1:
            self.direction = "DOWN"
        self.registered_time = self.env.now
        self.priority_array = None
    
    def __str__(self):
        """Returns a string representation of the HallCall object."""
        return f"Hall call from {self.source_floor} with {self.direction} direction. Priority array: {self.priority_array}"
    
    def get_source_floor(self)->int:
        """Returns source floor level"""
        return self.source_floor
    
    def get_direction(self)->str:
        """Returns direction of call"""
        return self.direction
    
    def get_registered_time(self)->float:
        """Returns time when the call is registered"""
        return self.registered_time
    
    def set_priority_array(self, array)->None:
        """Sets the priority array attribute for the HallCall"""
        self.priority_array = array

    def get_first_priority_value(self)->None:
        """Returns the first priority array value for the HallCall,
        which is the additional cost incurred if this hall call is assigned
        to the next best elevator"""
        return self.priority_array[0][1]
    
    def get_second_priority_value(self)->None:
        """Returns the second priority array value for the HallCall,
        which is the additional cost incurred if this hall call is assigned
        to the next best elevator"""
        return self.priority_array[1][1]
    
    def get_current_best_elevator(self)->None:
        """Returns the index of the current best elevator based on HCPM"""
        return self.priority_array[0][0]
    
    def get_current_second_best_elevator(self)->None:
        """Returns the index of the current best elevator based on HCPM"""
        return self.priority_array[1][0]
    
    def get_priority_array_length(self)->None:
        """Returns the current length of the priority array"""
        return len(self.priority_array)
    
    def remove_frontmost_array_pair(self)->None:
        """Removes the frontmost priority array pair"""
        self.priority_array = self.priority_array[1:]