import unittest
from bench_planner import (
    estimate_1rm,
    calculate_weekly_rate,
    calculate_reps_for_weight,
    round_to_nearest,
    generate_weekly_plan
)

class TestBenchPlanner(unittest.TestCase):

    def test_estimate_1rm(self):
        self.assertAlmostEqual(estimate_1rm((135, 5)), 157.5)

    def test_calculate_weekly_rate(self):
        rate = calculate_weekly_rate(157.5, 165, 2)
        self.assertAlmostEqual(rate, 0.02345, places=4)

    def test_calculate_reps_for_weight(self):
        reps = calculate_reps_for_weight(165, 135)
        self.assertEqual(reps, 7)

    def test_round_to_nearest(self):
        self.assertEqual(round_to_nearest(221.1, 2.5), 222.5)

    def test_unrealistic_progression_flag(self):
        # Simulate a short-term aggressive goal: 135 → 165 in 2 weeks
        current_1rm = 157.5  # Estimated from (135, 5)
        goal_1rm = 165
        timeframe = 2
        frequency = 1
        rate = calculate_weekly_rate(current_1rm, goal_1rm, timeframe)

        # Check if the projected weekly % increase is above a "safe" threshold
        safe_max_rate = 0.01  # e.g., 1% per week
        self.assertGreater(rate, safe_max_rate, msg="Progression rate is too aggressive, should trigger warning")

    def test_generate_plan_output_format(self):
        import io
        import sys

        # Redirect output to test printed content
        captured_output = io.StringIO()
        sys.stdout = captured_output

        generate_weekly_plan(current_1rm=157.5, rate=0.02345, weeks=2, frequency=1)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("Week 1", output)
        self.assertIn("Session 1", output)
        self.assertIn("Projected 1RM", output)

if __name__ == '__main__':
    unittest.main()
