from dataclasses import dataclass


class FlightData:
    """Клас для зберігання вхідних параметрів рейсу."""

    def __init__(
        self,
        distance: float,
        speed: float,
        base_fuel_rate: float,
        reserves_percent: float,
    ):
        self._distance = distance
        self._speed = speed
        self._base_fuel_rate = base_fuel_rate
        self._reserves_percent = reserves_percent

    def getDistance(self) -> float:
        return self._distance

    def getSpeed(self) -> float:
        return self._speed

    def getBaseFuelRate(self) -> float:
        return self._base_fuel_rate

    def getReservesPercent(self) -> float:
        return self._reserves_percent


@dataclass
class ResultData:
    """Клас для зберігання результатів розрахунку рейсу."""

    flight_time: float
    trip_fuel: float
    reserve_fuel: float
    total_fuel: float