import Building
import Elevator
import Person
import simpy
import random
import statistics



class Main(object):
    def __init__(self, num_elevators):
        self.env = simpy.Environment

    def run(self):
