import unittest

from calculator import FlightCalculator
from models import FlightData


class TestFlightCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = FlightCalculator()

    def test_valid_calculation(self):
        data = FlightData(distance=1600, speed=800, base_fuel_rate=2500, reserves_percent=15)
        result = self.calculator.processCalculation(data)

        self.assertAlmostEqual(result.flight_time, 2.0)
        self.assertAlmostEqual(result.trip_fuel, 5000.0)
        self.assertAlmostEqual(result.reserve_fuel, 750.0)
        self.assertAlmostEqual(result.total_fuel, 5750.0)

    def test_zero_speed_raises_error(self):
        data = FlightData(distance=1000, speed=0, base_fuel_rate=2000, reserves_percent=10)
        self.assertFalse(self.calculator.validateData(data))
        with self.assertRaises(ValueError):
            self.calculator.processCalculation(data)

    def test_negative_distance_raises_error(self):
        data = FlightData(distance=-500, speed=800, base_fuel_rate=2000, reserves_percent=10)
        self.assertFalse(self.calculator.validateData(data))
        with self.assertRaises(ValueError):
            self.calculator.processCalculation(data)

    def test_negative_reserves_raises_error(self):
        data = FlightData(distance=500, speed=800, base_fuel_rate=2000, reserves_percent=-5)
        self.assertFalse(self.calculator.validateData(data))

    def test_zero_reserves_is_valid(self):
        data = FlightData(distance=800, speed=800, base_fuel_rate=2000, reserves_percent=0)
        result = self.calculator.processCalculation(data)
        self.assertAlmostEqual(result.total_fuel, 2000.0)


if __name__ == "__main__":
    unittest.main()