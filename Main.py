import simpy
import statistics
import Building


class Main(object):
    def __init__(self, num_up, num_down, num_floors):
        self.env = simpy.Environment()
        self.num_up = num_up
        self.num_down = num_down
        self.num_floors = num_floors
        self.building = None

    def run(self, duration):
        self.building = Building.Building(self.env, self.num_up, self.num_down, self.num_floors)
        self.building.initialise()
        self.env.process(self.building.simulate())
        self.env.run(until=duration)


Test = Main(2, 2, 9)
Test.run(20000)
waiting_time = []
for i in x.building.all_persons_spawned:
    if i.has_completed_trip():
        waiting_time.append(i.get_wait_time())
print(statistics.mean(waiting_time))