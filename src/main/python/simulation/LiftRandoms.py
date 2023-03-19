from enum import Enum
import pandas as pd
import random as rd
import pathlib
import os

# changing working directory to file location
cur_dir = pathlib.Path(__file__).parent.resolve()
os.chdir(cur_dir)

# initializing proportion csv as Pandas dataframes
prop1 = pd.read_csv('../../../data/prop1.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop2 = pd.read_csv('../../../data/prop2.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop3 = pd.read_csv('../../../data/prop3.csv').iloc[:, 1:].sort_values('p', ascending=False)
prop4 = pd.read_csv('../../../data/prop4.csv').iloc[:, 1:].sort_values('p', ascending=False)


class DayPhase(Enum):
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2


class HourPhase(Enum):
    PRE_PEAK = 0
    PEAK = 1
    POST_PEAK_I = 2
    POST_PEAK_II = 3
    OFF_PEAK = 4


class LiftRandoms:
    """Wrapper class for functions to generate the random variables as required in LiftSim.

    No attributes.
    """

    def next_arrival_time(self, curr_time, max_lambda=167/900) -> float:
        """
        Generates the next arrival time of a rider according to a non-homogeneous Poisson process,
        using the thinning method.

        Args: 
            curr_time (float): Current timestamp of the environment in seconds
            max_lambda (float): Default value set to 167/900
        
        Returns:
            float: The next arrival time.
        """
        uniform_rv = rd.uniform(0, 1)
        arrival_time = curr_time + rd.expovariate(max_lambda)

        while uniform_rv > (self.thinning_fn(arrival_time)/max_lambda):
            arrival_time += rd.expovariate(max_lambda)
            uniform_rv = rd.uniform(0, 1)
        
        return arrival_time

    def thinning_fn(self, x) -> float:
        """
        Helper function for nextArrivalTime to augment the rate parameter of the Exp random variable.

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
        if day_phase == DayPhase.MORNING and hr_phase == HourPhase.OFF_PEAK:
            return 9/100
        if day_phase == DayPhase.MORNING and hr_phase == HourPhase.PEAK:
            return 127/900
        if day_phase == DayPhase.MORNING and hr_phase == HourPhase.POST_PEAK_I:
            return 1/12
        if day_phase == DayPhase.MORNING and hr_phase == HourPhase.POST_PEAK_II:
            return 11/225
        
        # afternoon: pre-peak, peak, post-peak1, post-peak2
        if day_phase == DayPhase.AFTERNOON and hr_phase == HourPhase.OFF_PEAK:
            return 19/150
        if day_phase == DayPhase.AFTERNOON and hr_phase == HourPhase.PEAK:
            return 167/900
        if day_phase == DayPhase.AFTERNOON and hr_phase == HourPhase.POST_PEAK_I:
            return 21/200
        if day_phase == DayPhase.AFTERNOON and hr_phase == HourPhase.POST_PEAK_II:
            return 29/600

        # evening: pre-peak, peak, post-peak1, post-peak2
        if day_phase == DayPhase.EVENING and hr_phase == HourPhase.OFF_PEAK:
            return 31/600
        if day_phase == DayPhase.EVENING and hr_phase == HourPhase.PEAK:
            return 7/75
        if day_phase == DayPhase.EVENING and hr_phase == HourPhase.POST_PEAK_I:
            return 3/50

    def generate_source_dest(self, x) -> tuple:
        """
        Generates a random source and destination floor for use in instantiating a Person class,
        according to data collected (see prop1.csv).
        Performed by ordered inversion method for discrete random variable simulation.

        Args:
            x (float): Simulation clock timestamp.
        
        Returns:
            source (int): Generated source floor for Person instantiation.
            destination (int): Generated destination floor for Person instantiation.
        """

        day_phase, hr_phase = self.phase(x)
        uniform_rv = rd.uniform(0, 1)
        probability = 0
        index = -1

        # initialize the correct proportions dataframe (off-peak, morning, evening, etc.)
        if hr_phase == HourPhase.OFF_PEAK:
            prop_data = prop1
        elif day_phase == DayPhase.MORNING:
            prop_data = prop2
        elif day_phase == DayPhase.AFTERNOON:
            prop_data = prop3
        else:
            prop_data = prop4

        # ordered sequential inversion method for discrete random variable simulation
        while uniform_rv > probability:
            index += 1
            probability += prop_data.iloc[index, 2]

        return tuple(prop_data.iloc[index, 0:2].astype('int'))

    @staticmethod
    def phase(arrival_time) -> tuple:
        """
        Helper function for the thinning method, to determine which part of the day it is in the simulation.

        Args:
            arrival_time (float): Proposed arrival time from nextArrivalTime.
        
        Returns:
            day_phase (int): Integer to represent the time of the day; morning=0, afternoon=1, evening=2.
            hr_phase (int): Integer to represent the peak-ness of the period;
                pre-peak=0, peak=1, post-peak1=2, post-peak2=3, off-peak=4.
        """

        # morning
        if arrival_time < 14400:
            day_phase = DayPhase.MORNING
        # afternoon
        elif arrival_time < 36000:
            day_phase = DayPhase.AFTERNOON
            arrival_time -= 14400
        # evening
        else:
            day_phase = DayPhase.EVENING
            arrival_time -= 36000

        # hr phases
        if arrival_time < 300:
            hr_phase = HourPhase.PRE_PEAK
        elif arrival_time < 1200:
            hr_phase = HourPhase.PEAK
        elif arrival_time < 1800:
            hr_phase = HourPhase.POST_PEAK_I
        elif arrival_time < 2700:
            hr_phase = HourPhase.POST_PEAK_II
        elif arrival_time < 7200:
            hr_phase = HourPhase.OFF_PEAK
        elif arrival_time < 7500:
            hr_phase = HourPhase.PRE_PEAK
        elif arrival_time < 8400:
            hr_phase = HourPhase.PEAK
        elif arrival_time < 9000:
            hr_phase = HourPhase.POST_PEAK_I
        elif arrival_time < 9900:
            hr_phase = HourPhase.POST_PEAK_II
        elif arrival_time < 14400:
            hr_phase = HourPhase.OFF_PEAK
        elif arrival_time < 14700:
            hr_phase = HourPhase.PRE_PEAK
        elif arrival_time < 15600:
            hr_phase = HourPhase.PEAK
        elif arrival_time < 16200:
            hr_phase = HourPhase.POST_PEAK_I
        elif arrival_time < 17100:
            hr_phase = HourPhase.POST_PEAK_II
        else:
            hr_phase = HourPhase.OFF_PEAK

        return day_phase, hr_phase
