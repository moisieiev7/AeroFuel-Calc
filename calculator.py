from models import FlightData, ResultData


class FlightCalculator:
    """Клас математичної логіки для обчислення часу польоту та пального."""

    def validateData(self, data: FlightData) -> bool:
        if data.getDistance() <= 0:
            return False
        if data.getSpeed() <= 0:
            return False
        if data.getBaseFuelRate() <= 0:
            return False
        if data.getReservesPercent() < 0:
            return False
        return True

    def calculateFlightTime(self, distance: float, speed: float) -> float:
        return distance / speed

    def calculateTotalFuel(self, time: float, rate: float, reserves: float) -> float:
        trip_fuel = time * rate
        reserve_fuel = trip_fuel * (reserves / 100.0)
        return trip_fuel + reserve_fuel

    def processCalculation(self, data: FlightData) -> ResultData:
        if not self.validateData(data):
            raise ValueError(
                "Некоректні дані: відстань, швидкість і витрата пального мають бути "
                "більшими за 0, а резерв — невід'ємним."
            )

        flight_time = self.calculateFlightTime(data.getDistance(), data.getSpeed())
        trip_fuel = flight_time * data.getBaseFuelRate()
        total_fuel = self.calculateTotalFuel(
            flight_time, data.getBaseFuelRate(), data.getReservesPercent()
        )
        reserve_fuel = total_fuel - trip_fuel

        return ResultData(
            flight_time=flight_time,
            trip_fuel=trip_fuel,
            reserve_fuel=reserve_fuel,
            total_fuel=total_fuel,
        )