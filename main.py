from abc import ABC, abstractmethod
import datetime
import pandas as pd
import pvlib
import time



class SolarPositionCalculatorInterface(ABC):
    """
    Interface for calculating solar position
    """
    @abstractmethod
    def calculate_solar_position(self):
        pass


class SolarPositionCalculator(SolarPositionCalculatorInterface):
    """
    Implementation of the solar position calculator
    """
    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude

    def calculate_solar_position(self):
        current_time = datetime.datetime.now()

        location = pvlib.location.Location(self.latitude, self.longitude)
        time = pd.Timestamp(current_time)
        solar_position = pvlib.solarposition.get_solarposition(time, location.latitude, location.longitude)
        solar_zenith_angle = solar_position['apparent_zenith'].iloc[0]

        return solar_zenith_angle


class SolarPanelCorrector:
    """
   Correction of the solar panel position
    """
    def __init__(self, position_calculator: SolarPositionCalculatorInterface):
        self.position_calculator = position_calculator

    def correct_solar_panel_position(self):
        solar_zenith_angle = self.position_calculator.calculate_solar_position()
        # Your correction logic goes here
        print(f"Solar panel position corrected. Solar Zenith Angle: {solar_zenith_angle:.2f} degrees")


class SolarPanelController:
    """
    The solar panel system manager
    """
    def __init__(self, correction_interval_minutes: int, panel_size: str, corrector: SolarPanelCorrector):
        self.correction_interval_minutes = correction_interval_minutes
        self.panel_size = panel_size
        self.corrector = corrector

    def set_correction_interval(self, minutes):
        """
        Set the interval (in minutes) for solar panel correction.
        """
        self.correction_interval_minutes = minutes

    def set_panel_size(self, size):
        """
        Set the size of the solar panel.
        """
        self.panel_size = size

    def run_correction_scheduler(self):
        """
        Run the solar panel correction at the specified interval.
        """
        while True:
            self.corrector.correct_solar_panel_position()
            time.sleep(self.correction_interval_minutes * 60)  # Convert minutes to seconds

