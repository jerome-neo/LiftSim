import pandas as pd
import random as rd
import pathlib
import os

# changing working directory to file location
cur_dir = pathlib.Path(__file__).parent.resolve()
os.chdir(cur_dir)

# initializing proportion csv as Pandas dataframes
prop1 = pd.read_csv('../../data analysis/prop1.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop2 = pd.read_csv('../../data analysis/prop2.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop3 = pd.read_csv('../../data analysis/prop3.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop4 = pd.read_csv('../../data analysis/prop4.csv').iloc[:, 1:].sort_values('p', ascending=False)

class LiftRandoms:
    """Wrapper class for functions to generate the random variables as required in LiftSim.

    No attributes.
    """

    def next_arrival_time(self, cur_time, maxlambda=167/900) -> float:
        """Generates the next arrival time of a rider according to a non-homogeneous Poisson process, using the thinning method.

        Args: 
            cur_time (float): Current timestamp of the environment in seconds
        
        Returns:
            float: The next arrival time.
        """
        u = rd.uniform(0, 1)
        arr_time = cur_time + rd.expovariate(maxlambda)

        while u > (self.thinning_fn(arr_time)/maxlambda):
            arr_time += rd.expovariate(maxlambda)
            u = rd.uniform(0, 1)
        
        return arr_time

    def thinning_fn(self, x) -> float:
        """Helper function for nextArrivalTime to augment the rate parameter of the Exp random variable.

        Args:
            x (float): Proposed arrival time from next_arrival_time.

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

    def generate_source_dest(self, x) -> tuple:
        """Generates a random source and destination floor for use in instantiating a Person class, according to data collected (see prop1.csv).
           Performed by ordered inversion method for discrete random variable simulation.

        Args:
            x (float): Simulation clock timestamp.
        
        Returns:
            source (int): Generated source floor for Person instantiation.
            destination (int): Generated destination floor for Person instantiation.
        """

        day_phase, hr_phase = self.phase(x)
        u = rd.uniform(0, 1)
        p = 0
        i = -1

        # initialize the correct proportions dataframe (off-peak, morning, evening, etc.)
        if hr_phase == 4:
            prop_data = prop1
        elif day_phase == 0:
            prop_data = prop2
        elif day_phase == 1:
            prop_data = prop3
        else:
            prop_data = prop4

        # ordered sequential inversion method for discrete random variable simulation
        while u > p:
            i += 1
            p += prop_data.iloc[i, 2]

        return tuple(prop_data.iloc[i, 0:2].astype('int'))

    def phase(self, x) -> tuple:
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
