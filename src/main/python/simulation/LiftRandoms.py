import random as rd

class LiftRandoms:
    """Wrapper class for functions to generate the random variables as required in LiftSim.

    No attributes.
    """

    def nextArrivalTime(self, cur_time, thin_fn, maxlambda=167/900):
        """Generates the next arrival time of a rider according to a non-homogeneous Poisson process, using the thinning method.

        Args: 
            cur_time (float): Current timestamp of the environment in seconds.
            thin_fn (function): Thinning function from LiftRandoms class, defined below.
        
        Returns:
            float: The next arrival time.
        """
        u = rd.uniform(0, 1)
        arr_time = cur_time + rd.expovariate(maxlambda)

        while u > (thin_fn(arr_time)/maxlambda):
            arr_time += rd.expovariate(maxlambda)
            u = rd.uniform(0, 1)
        
        return arr_time

    def thinning_fn(self, x):
        """Helper function for nextArrivalTime to augment the rate parameter of the Exp random variable.

        Args:
            x (float): Proposed arrival time from nextArrivalTime.

        Returns:
            float: The corresponding rate parameter at the proposed arrival time.
        """

        day_phase, hr_phase = self.phase(x)

        # off-peak
        if hr_phase == 4:
            return 14/225

        # morning: pre-peak, peak, post-peak1, post-peak2
        if day_phase == 0 and hr_phase == 0:
            return 9/100
        if day_phase == 0 and hr_phase == 1:
            return 127/900
        if day_phase == 0 and hr_phase == 2:
            return 1/12
        if day_phase == 0 and hr_phase == 3:
            return 11/225
        
        # afternoon: pre-peak, peak, post-peak1, post-peak2
        if day_phase == 1 and hr_phase == 0:
            return 19/150
        if day_phase == 1 and hr_phase == 1:
            return 167/900
        if day_phase == 1 and hr_phase == 2:
            return 21/200
        if day_phase == 1 and hr_phase == 3:
            return 29/600

        # evening: pre-peak, peak, post-peak1, post-peak2
        if day_phase == 2 and hr_phase == 0:
            return 31/600
        if day_phase == 2 and hr_phase == 1:
            return 7/75
        if day_phase == 2 and hr_phase == 2:
            return 3/50

    def phase(self, x):
        """Helper function for the thinning method, to determine which part of the day it is in the simulation.

        Args:
            x (float): Proposed arrival time from nextArrivalTime.
        
        Returns:
            day_phase (int): Integer to represent the time of the day; morning=0, afternoon=1, evening=2.
            hr_phase (int): Integer to represent the peak-ness of the period; pre-peak=0, peak=1, post-peak1=2, post-peak2=3, off-peak=4.
        """

        # morning
        if x < 14400:
            day_phase = 0
        
        # afternoon
        elif x < 36000:
            day_phase = 1
            x -= 14400
        
        # evening
        else:
            day_phase = 2
            x -= 36000

        # hr phases
        if x < 300:
            hr_phase = 0
        elif x < 1200:
            hr_phase = 1
        elif x < 1800:
            hr_phase = 2
        elif x < 2700:
            hr_phase = 3
        elif x < 7200:
            hr_phase = 4
        elif x < 7500:
            hr_phase = 0
        elif x < 8400:
            hr_phase = 1
        elif x < 9000:
            hr_phase = 2
        elif x < 9900:
            hr_phase = 3
        elif x < 14400:
            hr_phase = 4
        elif x < 14700:
            hr_phase = 0
        elif x < 15600:
            hr_phase = 1
        elif x < 16200:
            hr_phase = 2
        elif x < 17100:
            hr_phase = 3
        else:
            hr_phase = 4

        return (day_phase, hr_phase)
