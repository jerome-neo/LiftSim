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
            direction(int): direction of elevator call -> -1 if down, 1 if up

        """
        self.env = env
        self.source_floor = source_floor
        if direction > 0:
            self.direction = "UP"
        else:
            self.direction = "DOWN"
        self.registered_time = self.env.now
    
    def get_source_floor(self)->int:
        """Returns source floor level"""
        return self.source_floor
    
    def get_direction(self)->str:
        """Returns direction of call"""
        return self.direction
    
    def get_registered_time(self)->float:
        """Returns time when the call is registered"""
        return self.registered_time