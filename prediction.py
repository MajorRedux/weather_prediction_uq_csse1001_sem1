"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = "Richard Roth"
__email__ = "r.roth@uqconnect.edu.au"

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


# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.
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

    def get_number_days(self):
        """(int) Returns number of days of data being used"""
        return self._simple_prediction.get_number_days()

    def chance_of_rain(self):
        """(int) Calculates the average rainfall for the past n days"""
        total_rainfall = 0
        n = 0
        # for each row get the rainfall, add it to total rainfall and increase n by 1
        for row in self._simple_prediction:
            total_rainfall += self._simple_prediction[n].get_rainfall()
            n += 1
        total_rainfall /= n * 9
        if total_rainfall > 100:
            total_rainfall = 100

        return total_rainfall

    def high_temperature(self):
        """(float) Returns the highest temperature in n days"""
        max_temperature = 0.0
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
        min_temperature = 0.0
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
        total_humidity = 0
        n = 0
        # for each row get the humidity, add it to total humidity and increase n by 1
        for row in self._simple_prediction:
            total_humidity += self._simple_prediction[n].get_humidity()
            n += 1
        total_humidity /= n
        return total_humidity

    def cloud_cover(self):
        """(int) Calculates average cloud cover over n days"""
        total_cloud_cover = 0
        n = 0
        # for each row get the cloud cover, add it to total total and increase n by 1
        for row in self._simple_prediction:
            total_cloud_cover += self._simple_prediction[n].get_cloud_cover()
            n += 1
        total_cloud_cover /= n
        return total_cloud_cover

    def wind_speed(self):
        """(int) Calculates average wind speed over n days from average wind speed per pay."""
        total_average_wind_speed = 0
        n = 0
        for row in self._simple_prediction:
            total_average_wind_speed += self._simple_prediction[n].get_average_wind_speed(
            )
            n += 1
        total_average_wind_speed /= n
        return total_average_wind_speed


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
        if n_days > weather_data.size():
            n_days = weather_data.size()
        self._sophisticated_prediction = self._weather_data.get_data(n_days)

    def get_number_days(self):
        """(int) Returns number of days of data being used"""
        return self._sophisticated_prediction.get_number_days()

    def chance_of_rain(self):
        """(int) Calculates the average rainfall for the past n days"""
        total_rainfall = 0
        n = 0
        easterly_wind_direction = ("NNE", "NE", "ENE", "E", "ESE", "SE", "SSE")
        # for each row get the rainfall, add it to total rainfall and increase n by 1
        for row in self._sophisticated_prediction:
            total_rainfall += self._sophisticated_prediction[n].get_rainfall()
            n += 1
        total_rainfall /= n
        if self._sophisticated_prediction[0].get_air_pressure() > air_pressure():
            total_rainfall *= 10
        elif self._sophisticated_prediction[0].get_air_pressure() >= air_pressure():
            total_rainfall * 7
        elif self._sophisticated_prediction[0].get_wind_direction() in easterly_wind_direction:
            total_rainfall * 1.2

        if total_rainfall > 100:
            total_rainfall = 100
        return total_rainfall

    def air_pressure(self):
        """(float) Calculates the average air pressure for the past n days"""
        total_air_pressure = 0
        n = 0
        # for each row get the air pressure, add it to total air pressure and increase n by 1
        for row in self._sophisticated_prediction:
            total_air_pressure += self._sophisticated_prediction[n].get_air_pressure(
            )
            n += 1
        total_air_pressure /= n
        return total_air_pressure

    def high_temperature(self):
        """(float) Returns the highest temperature in n days"""
        max_temperature = 0.0
        n = 0
        # for each row in weather data find high temperature and compare it to max temperature
        for row in self._simple_prediction:
            if self._simple_prediction[n].get_high_temperature() > max_temperature:
                max_temperature = self._simple_prediction[n].get_high_temperature(
                )
            n += 1
        if self._sophisticated_prediction[0].get_air_pressure() < air_pressure():
            max_temperature += 2
        return max_temperature

    def low_temperature(self):
        """(float) Returns the lowest temperature in n days"""
        min_temperature = 0.0
        n = 0
        # for each row in weather data find low temperature and compare it with min temperature
        for row in self._simple_prediction:
            if self._simple_prediction[n].get_low_temperature() < min_temperature:
                min_temperature = self._simple_prediction[n].get_low_temperature(
                )
            n += 1
        if self._sophisticated_prediction[0].get_air_pressure() > air_pressure():
            max_temperature -= 2
        return min_temperature

    def humidity(self):
        """(int) Calculates average humidity over n days"""
        total_humidity = 0
        n = 0
        # for each row get the humidity, add it to total humidity and increase n by 1
        for row in self._simple_prediction:
            total_humidity += self._simple_prediction[n].get_humidity()
            n += 1
        total_humidity /= n

        if self._sophisticated_prediction[0].get_air_pressure() > air_pressure():
            total_humidity += 15
        elif self._sophisticated_prediction[0].get_air_pressure() < air_pressure():
            total_humidity -= 15

        if total_humidity > 100:
            total_humidity = 100
        elif total_humidity < 0:
            total_humidity = 0
        return total_humidity

    def cloud_cover(self):
        """(int) Calculates average cloud cover over n days"""
        total_cloud_cover = 0
        n = 0
        # for each row get the cloud cover, add it to total total and increase n by 1
        for row in self._simple_prediction:
            total_cloud_cover += self._simple_prediction[n].get_cloud_cover()
            n += 1
        total_cloud_cover /= n

        if self._sophisticated_prediction[0].get_air_pressure() < air_pressure():
            total_cloud_cover += 2
        if total_cloud_cover > 9:
            total_cloud_cover = 9
        return total_cloud_cover

    def wind_speed(self):
        """(int) Calculates average wind speed over n days from average wind speed per pay."""
        total_average_wind_speed = 0
        n = 0
        for row in self._simple_prediction:
            total_average_wind_speed += self._simple_prediction[n].get_average_wind_speed(
            )
            n += 1
        total_average_wind_speed /= n
        if self._sophisticated_prediction[0].get_maximum_wind_speed() > (total_average_wind_speed * 4):
            total_average_wind_speed * 1.2
        return total_average_wind_speed


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
