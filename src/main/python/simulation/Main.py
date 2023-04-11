import sys
import csv
import json
import simpy
import statistics

sys.path.append('c:/Users/dorot/OneDrive - National University of Singapore/DSA3101/DSA3101-07-S16/')

import src.main.python.simulation.Building as Building
from src.main.python.simulation.PersonList import PersonList


class Main(object):
    """
    Represents the main simulation object that initializes and runs the simulation.

    Attributes:
        num_up (int): The number of elevators that move upwards.
        num_down (int): The number of elevators that move downwards.
        num_floors (int): The number of floors in the building.
    """

    def __init__(self, num_up, num_down, num_floors):
        """
        Initializes a new instance of the Main class.

        Args:
            num_up (int): The number of elevators that move upwards.
            num_down (int): The number of elevators that move downwards.
            num_floors (int): The number of floors in the building.

        """
        self.env = simpy.Environment()
        self.num_up = num_up
        self.num_down = num_down
        self.num_floors = num_floors
        self.building = None
        self.person_list = None
        self.lift_algos = ['Otis', 'ModernEGCS']

    def run(self, duration, mode='default'):
        """
        Runs the simulation for a specified duration.

        Args:
            duration (float): The duration of the simulation in seconds.
            mode (string): 'default' or 'manual'
        """
        self.person_list = PersonList(self.env, duration, limit=500)  # person generated cannot exceed 300
        self.person_list.initialise(mode=mode)
        
        for lift_algo in self.lift_algos:
            print(f"Running S16 elevator simulation with {lift_algo} algorithm")
            self.building = Building.Building(self.env, self.num_up, self.num_down, self.num_floors, self.person_list)
            self.building.initialise(lift_algo)
            self.env.process(self.building.simulate())
            while self.env.peek() < duration:
                self.env.step()
            self.output_person_to_csv(lift_algo)
            self.output_person_to_json(lift_algo)
            self.output_elevator_log_to_json(lift_algo)

            # Additional information to be printed in terminal
            print('Number of people spawned in advance:', len(self.building.get_all_persons()))
            print('Number of people served:', self.get_number_of_people_served())
            print(f"Average waiting time for {lift_algo}: {self.get_average_waiting_time()}")

            self.env = simpy.Environment()
            self.person_list.reset(self.env)

    def get_average_waiting_time(self):
        waiting_time = []
        people = self.person_list.get_person_list()
        for person in people:
            if person.has_completed_trip():
                waiting_time.append(person.get_wait_time())

        if len(waiting_time) == 0:
            return -1
        else:
            return statistics.mean(waiting_time)

    def get_number_of_people_served(self):
        people = self.person_list.get_person_list()
        return len(list(filter(lambda x: x.has_completed_trip(), people)))

    def output_person_to_csv(self, lift_algo, path='../../out/'):
        name = 'output_persons_'+lift_algo+'.csv'
        header = ['curr', 'dest', 'arrival_time', 'end_time', 'wait_time']
        data = []
        for person in self.person_list.get_person_list():
            if person.has_completed_trip():
                curr = person.get_curr_floor()
                dest = person.get_dest_floor()
                arrival_time = person.get_arrival_time()
                end_time = person.get_end_time()
                wait_time = person.get_wait_time()
                data.append([curr, dest, arrival_time, end_time, wait_time])
        with open(path + name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

    def output_person_to_json(self, lift_algo, path='../../out/'):
        name = 'output_persons_'+lift_algo+'.json'
        data = []
        for person in self.person_list.get_person_list():
            if person.has_completed_trip():
                curr = int(person.get_curr_floor())
                dest = int(person.get_dest_floor())
                arrival_time = float(person.get_arrival_time())
                end_time = float(person.get_end_time())
                wait_time = float(person.get_wait_time())
                data.append({
                    'curr': curr,
                    'dest': dest,
                    'arrival_time': arrival_time,
                    'end_time': end_time,
                    'wait_time': wait_time
                })
        with open(path + name, 'w', encoding='UTF8') as f:
            json.dump(data, f, indent=4)

    def output_elevator_log_to_json(self, lift_algo, path='../../out/'):
        name = 'output_elevator_'+lift_algo+'.json'
        json_serializable = json.dumps(self.building.to_dict(), indent=4)
        with open(path + name, 'w') as f:
            f.write(json_serializable)
    

# Example ways of running the simulation

# Step 1
# set up the environment with number of UP elevators, number of DOWN elevators and number of floors"
Test = Main(num_up=2, num_down=1, num_floors=9)

# Step 2
# run the simulation by telling it how long to run, e.g. 6800 (from 6 am to 12 am at the same day)
with open('output.txt', 'w') as f:
    # Redirect standard output to the file
    sys.stdout = f
    Test.run(64800, mode='default')
