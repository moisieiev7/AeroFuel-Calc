import tkinter as tk
from tkinter import messagebox, ttk

from calculator import FlightCalculator
from models import FlightData, ResultData


class MainForm:
    """Клас графічного інтерфейсу користувача AeroFuel Calc."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AeroFuel Calc — Калькулятор авіаційного пального")
        self.root.geometry("480x440")
        self.root.resizable(False, False)

        self.calculator = FlightCalculator()
        self.unit_system = tk.StringVar(value="metric")

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            main_frame,
            text="AeroFuel Calc",
            font=("Helvetica", 16, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

        units_frame = ttk.LabelFrame(main_frame, text="Одиниці виміру", padding=8)
        units_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))

        ttk.Radiobutton(
            units_frame,
            text="Метричні (км, км/год, кг)",
            variable=self.unit_system,
            value="metric",
            command=self._update_unit_labels,
        ).pack(anchor="w")

        ttk.Radiobutton(
            units_frame,
            text="Авіаційні (морські милі, вузли, фунти)",
            variable=self.unit_system,
            value="aviation",
            command=self._update_unit_labels,
        ).pack(anchor="w")

        self.distance_lbl = ttk.Label(main_frame, text="Відстань (км):")
        self.distance_lbl.grid(row=2, column=0, sticky="w", pady=5)
        self.distanceInput = ttk.Entry(main_frame, width=22)
        self.distanceInput.grid(row=2, column=1, sticky="e", pady=5)

        self.speed_lbl = ttk.Label(main_frame, text="Крейсерська швидкість (км/год):")
        self.speed_lbl.grid(row=3, column=0, sticky="w", pady=5)
        self.speedInput = ttk.Entry(main_frame, width=22)
        self.speedInput.grid(row=3, column=1, sticky="e", pady=5)

        self.fuel_lbl = ttk.Label(main_frame, text="Базова витрата пального (кг/год):")
        self.fuel_lbl.grid(row=4, column=0, sticky="w", pady=5)
        self.fuelRateInput = ttk.Entry(main_frame, width=22)
        self.fuelRateInput.grid(row=4, column=1, sticky="e", pady=5)

        ttk.Label(main_frame, text="Обов'язковий резерв (%):").grid(
            row=5, column=0, sticky="w", pady=5
        )
        self.reservesInput = ttk.Entry(main_frame, width=22)
        self.reservesInput.insert(0, "15")
        self.reservesInput.grid(row=5, column=1, sticky="e", pady=5)

        self.calculateButton = ttk.Button(
            main_frame, text="Розрахувати", command=self._on_calculate
        )
        self.calculateButton.grid(row=6, column=0, columnspan=2, pady=15, sticky="ew")

        result_frame = ttk.LabelFrame(main_frame, text="Результати розрахунку", padding=10)
        result_frame.grid(row=7, column=0, columnspan=2, sticky="ew")

        self.resultLabel = ttk.Label(
            result_frame,
            text="Введіть параметри рейсу та натисніть «Розрахувати».",
            justify=tk.LEFT,
        )
        self.resultLabel.pack(anchor="w")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def _update_unit_labels(self):
        if self.unit_system.get() == "metric":
            self.distance_lbl.config(text="Відстань (км):")
            self.speed_lbl.config(text="Крейсерська швидкість (км/год):")
            self.fuel_lbl.config(text="Базова витрата пального (кг/год):")
        else:
            self.distance_lbl.config(text="Відстань (морські милі):")
            self.speed_lbl.config(text="Крейсерська швидкість (вузли):")
            self.fuel_lbl.config(text="Базова витрата пального (фунти/год):")

    def collectData(self) -> FlightData:
        try:
            distance = float(self.distanceInput.get().replace(",", ".").strip())
            speed = float(self.speedInput.get().replace(",", ".").strip())
            fuel_rate = float(self.fuelRateInput.get().replace(",", ".").strip())
            reserves = float(self.reservesInput.get().replace(",", ".").strip())
        except ValueError:
            raise ValueError("Будь ласка, вводьте лише числові значення в усі поля.")

        return FlightData(distance, speed, fuel_rate, reserves)

    def _on_calculate(self):
        try:
            flight_data = self.collectData()
            result = self.calculator.processCalculation(flight_data)
            self.displayResults(result)
        except ValueError as error:
            self.showError(str(error))

    def displayResults(self, result: ResultData):
        fuel_unit = "кг" if self.unit_system.get() == "metric" else "фунтів"
        hours = int(result.flight_time)
        minutes = round((result.flight_time - hours) * 60)
        if minutes == 60:
            hours += 1
            minutes = 0

        text = (
            f"Чистий час польоту: {hours} год {minutes} хв ({result.flight_time:.2f} год)\n"
            f"Пальне на маршрут (Trip Fuel): {result.trip_fuel:.2f} {fuel_unit}\n"
            f"Обов'язковий резерв: {result.reserve_fuel:.2f} {fuel_unit}\n"
            f"Загальний об'єм пального: {result.total_fuel:.2f} {fuel_unit}"
        )
        self.resultLabel.config(text=text)

    def showError(self, message: str):
        messagebox.showerror("Помилка вводу", message)