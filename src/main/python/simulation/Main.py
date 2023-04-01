import csv
import json
import simpy
import statistics
import Building
import sys
from PersonList import PersonList

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

    def run(self, duration, lift_algo, mode = 'default'):
        """
        Runs the simulation for a specified duration.

        Args:
            duration (float): The duration of the simulation in seconds.
            lift_algo (string): The type of lift algo ran by the simulation

        """
        print(f"Running S16 elevator simulation with {lift_algo} algorithm")
        self.person_list = PersonList(self.env,duration, limit=300) # person generated cannot exceed 300
        self.person_list.initialise(mode=mode)
        self.building = Building.Building(self.env,
                                          self.num_up,
                                          self.num_down,
                                          self.num_floors,
                                          self.person_list)
        self.building.initialise(lift_algo)
        self.env.process(self.building.simulate())
        
        while self.env.peek() < duration:
            self.env.step()

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

    def output_person_to_csv(self, path='../../out/'):
        name = 'output_persons.csv'
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

    def output_person_to_json(self, path='../../out/'):
        name = 'output_persons.json'
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

    def output_elevator_log_to_json(self, path='../../out/'):
        name = 'output_elevator.json'
        json_serializable = json.dumps(self.building.to_dict(), indent=4)
        with open(path + name, 'w') as f:
            f.write(json_serializable)


with open('output.txt', 'w') as f:
    sys.stdout = f
# Example ways of running the simulation

    # Step 1
    # set up the environment with number of UP elevators, number of DOWN elevators and number of floors"
    Test = Main(num_up=2, num_down=1, num_floors=9)

    # Step 2
    # run the simulation by telling it how long to run, e.g. 200
    # when mode is 'manual', it will read the input file in ../../in
    #Test.run(200, 'Otis', mode='manual') 
    #Test.run(200, 'Otis', mode='default')
    Test.run(200, 'ModernEGCS', mode='manual') 
    #Test.run(200, 'ModernEGCS', mode='default')

    # Step 3
    # Save the data of all persons that have completed their trip in the simulation
    Test.output_person_to_csv()
    Test.output_person_to_json()
    Test.output_elevator_log_to_json()

    # Additional information to be printed in terminal
    print('Number of people spawned in advance:', len(Test.building.get_all_persons()))
    print('Number of people served:', Test.get_number_of_people_served())
    print(Test.get_average_waiting_time())