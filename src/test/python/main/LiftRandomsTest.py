import unittest
from src.main.python.simulation.LiftRandoms import LiftRandoms, DayPhase


class LiftRandomsTest(unittest.TestCase):

    def test_generate_non_null_tuple(self):
        self.assertEqual(type(LiftRandoms().generate_source_dest(99)), tuple)
        self.assertEqual(len(LiftRandoms().generate_source_dest(99)), 2)

    def test_generate_phase_returns_correct_phase(self):
        day_phases = {14399: DayPhase.MORNING, 35999: DayPhase.AFTERNOON, 36000: DayPhase.EVENING}
        for time, phase in day_phases.items():
            self.assertEqual(LiftRandoms.phase(time)[0], phase)


if __name__ == '__main__':
    unittest.main()
