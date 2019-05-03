"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = "Richard Roth"
__email__ = "r.roth@uqconnect.edu.au"

# weather data imported from weather_data.py
from weather_data import WeatherData

class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


class SimplePrediction(WeatherPrediction):
    """Simple prediction model that predicts weather based on the average of the past n days' worth of data, where n is a parameter.
    """

    def __init__(self, weather_data, n_days):
        """
        Parameters:
            weather_Data (WeatherData): Collection of weather data.
            n_days (int): number of days worth of data

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        if n_days > weather_data.size():
            n_days = weather_data.size()
        self._simple_prediction = self._weather_data.get_data(n_days)
        self._yesterday_value = self._simple_prediction[0]
        self._number_days = n_days

    def get_number_days(self):
        """(int) Returns number of days of data being used"""
        return self._number_days

    def calculate_average(self, data):
        """
        Calculate the average value from the data

        Parameters :
            data (str): data gathered from WeatherData

        Return:
            (float) average
        """
        running_average = 0
        for row in self._simple_prediction:
            running_average += getattr(row, data)()
        total_average = running_average/self._number_days
        return total_average

    def chance_of_rain(self):
        """(int) Calculates the average rainfall for the past n days"""
        total_rainfall = self.calculate_average("get_rainfall")
        total_rainfall *= 9
        # value parameters
        if total_rainfall > 100:
            total_rainfall = 100
        return round(total_rainfall)

    def high_temperature(self):
        """(float) Returns the highest temperature in n days"""
        max_temperature = self._yesterday_value.get_high_temperature()
        n = 0
        # for each row in weather data find high temperature and compare it to max temperature
        for row in self._simple_prediction:
            if self._simple_prediction[n].get_high_temperature() > max_temperature:
                max_temperature = self._simple_prediction[n].get_high_temperature(
                )
            n += 1
        return max_temperature

    def low_temperature(self):
        """(float) Returns the lowest temperature in n days"""
        min_temperature = self._yesterday_value.get_low_temperature()
        n = 0
        # for each row in weather data find low temperature and compare it with min temperature
        for row in self._simple_prediction:
            if self._simple_prediction[n].get_low_temperature() < min_temperature:
                min_temperature = self._simple_prediction[n].get_low_temperature(
                )
            n += 1
        return min_temperature

    def humidity(self):
        """(int) Calculates average humidity over n days"""
        return round(self.calculate_average("get_humidity"))

    def cloud_cover(self):
        """(int) Calculates average cloud cover over n days"""
        return round(self.calculate_average("get_cloud_cover"))

    def wind_speed(self):
        """(int) Calculates average wind speed over n days from average wind speed per pay."""
        return round(self.calculate_average("get_average_wind_speed"))


class SophisticatedPrediction(WeatherPrediction):
    """Sophisticated prediction model that predicts weather based on n days worth of weather data
    """

    def __init__(self, weather_data, n_days):
        """
        Parameters:
            weather_Data (WeatherData): Collection of weather data.
            n_days (int): number of days worth of data

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        # restricts data set size
        if n_days > weather_data.size():
            n_days = weather_data.size()
        self._sophisticated_prediction = self._weather_data.get_data(n_days)
        self._yesterday_value = self._sophisticated_prediction[-1]
        self._number_days = n_days

    def get_number_days(self):
        """(int) Returns number of days of data being used"""
        return self._number_days

    def calculate_average(self, data):
        """
        Calculate the average value from the data

        Parameters :
            data (str): data gathered from WeatherData

        Return:
            (float) average
        """
        running_average = 0
        # for each row in the data set, get appropriate value and use appropriate method
        for row in self._sophisticated_prediction:
            running_average += getattr(row, data)()
        total_average = running_average/self._number_days
        return total_average
        
    def air_pressure(self):
        """(int) Calculates the average air pressure for the past n days."""
        return round(self.calculate_average("get_air_pressure"))

    def chance_of_rain(self):
        """(int) Calculates the average rainfall for the past n days"""
        total_average_rainfall = self.calculate_average("get_rainfall")
        easterly_wind_direction = ("NNE", "NE", "ENE", "E", "ESE", "SE", "SSE")
        # value parameters
        if self._yesterday_value.get_air_pressure() < self.air_pressure():
            total_average_rainfall = total_average_rainfall * 10
        if self._yesterday_value.get_air_pressure() >= self.air_pressure():
            total_average_rainfall = total_average_rainfall * 7
        if self._yesterday_value.get_wind_direction() in easterly_wind_direction:
            total_average_rainfall = total_average_rainfall * 1.2
        if total_average_rainfall > 100:
            total_average_rainfall = 100
        return round(total_average_rainfall)

    def high_temperature(self):
        """(float) Returns the highest temperature in n days"""
        total_average_temperature = self.calculate_average("get_high_temperature")
        # value parameters
        if self._yesterday_value.get_air_pressure() > self.air_pressure():
            total_average_temperature = total_average_temperature + 2
        return total_average_temperature

    def low_temperature(self):
        """(float) Returns the lowest temperature in n days"""
        total_average_temperature = self.calculate_average("get_low_temperature")
        # value parameters
        if self._yesterday_value.get_air_pressure() < self.air_pressure():
            total_average_temperature = total_average_temperature - 2
        return total_average_temperature

    def humidity(self):
        """(int) Calculates average humidity over n days"""
        total_humidity = self.calculate_average("get_humidity")
        # value parameters
        if self._yesterday_value.get_air_pressure() < self.air_pressure():
            total_humidity += 15
        if self._yesterday_value.get_air_pressure() > self.air_pressure():
            total_humidity -= 15
        if total_humidity > 100:
            total_humidity = 100
        if total_humidity < 0:
            total_humidity = 0
        return round(total_humidity)

    def cloud_cover(self):
        """(int) Calculates average cloud cover over n days"""
        average_total_cloud_cover = self.calculate_average("get_cloud_cover")
        # value parameters
        if self._yesterday_value.get_air_pressure() < self.air_pressure():
            average_total_cloud_cover = average_total_cloud_cover + 2
        if average_total_cloud_cover > 9:
            average_total_cloud_cover = 9
        return round(average_total_cloud_cover)

    def wind_speed(self):
        """(int) Calculates average wind speed over n days from average wind speed per pay."""
        total_average_wind_speed = self.calculate_average("get_average_wind_speed")
        # value parameters
        if self._yesterday_value.get_maximum_wind_speed() > (total_average_wind_speed * 4):
            total_average_wind_speed *= 1.2
        return round(total_average_wind_speed)


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
