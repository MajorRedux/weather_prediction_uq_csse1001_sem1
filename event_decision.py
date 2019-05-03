"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = "Richard Roth"
__email__ = "r.roth@uqconnect.edu.au"

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
class Event(object):
    """Holds data about a single event and provides access to that data."""

    def __init__(self, name, outdoors, cover_available, time):
        """Construct an event object based on name, whether it is outdoors, cover available and time.

        Parameters:
            name (string) : Name of an event
            outdoors (bool) : Whether event is outdoors
            cover_available (bool) : Whether cover is available
            time (int) : Integer from 0 up to but not including 24, indicating closest starting time to event.

            Return:
            __str__() : String representation in the following format: 'Event(name @ time, outdoors, cover_available)', ex: 'Event(Party @ 12,True, False)'
        """
        self._name = name
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._time = time

    def get_name(self):
        """Get name of the event"""
        return self._name

    def get_time(self):
        """Get time of the event"""
        return self._time

    def get_outdoors(self):
        """Return whether event is outdoors"""
        return self._outdoors

    def get_cover_available(self):
        """Return whether event cover is available"""
        return self._cover_available

    def __str__(self):
        """String representation of event."""
        return 'Event({0} @ {1}, {2}, {3})'.format(self._name, self._time, self._outdoors, self._cover_available)


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        temperature_factor = 0
        time = self._event.get_time()
        outdoors = self._event.get_outdoors()
        cover_available = self._event.get_cover_available()
        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()
        adjusted_high_temperature = high_temperature
        adjusted_low_temperature = low_temperature
        wind_speed = self._prediction_model.wind_speed()
        cloud_cover = self._prediction_model.cloud_cover()
        humidity = self._prediction_model.humidity()
        # adjusted_humidity: Rule 1
        if humidity > 70:
            humidity_factor = humidity/20
            if high_temperature >= 0 or low_temperature >= 0:
                adjusted_high_temperature = adjusted_high_temperature + humidity_factor
                adjusted_low_temperature = adjusted_low_temperature + humidity_factor
            elif high_temperature < 0 or low_temperature < 0:
                adjusted_high_temperature = adjusted_high_temperature - humidity_factor
                adjusted_low_temperature = adjusted_low_temperature - humidity_factor
        elif humidity <= 70:
            humidity_factor = humidity
        # initial temperature factor
        # rule 2a: time between 6 and 19 inclusive, event is outdoors and AHT is between 30; use formula AHT / -5 + 6
        if (time >= 6 and time <= 19) and outdoors and (adjusted_high_temperature >= 30):
            temperature_factor = adjusted_high_temperature / -5 + 6
        # rule 2b: AHT greater than or equal to 45; use formula AHT / -5 + 6
        elif adjusted_high_temperature >= 45:
            temperature_factor = adjusted_high_temperature / -5 + 6
        # rule 2c: time between 0 and 5 inclusive or between 20 and 23 inclusive and ALT is less than five or AHT is greater than 45; use formula ALT / 5 - 1.1
        elif ((time >= 0 and time <= 5) or (time >= 20 and time <= 23)) and (adjusted_low_temperature < 5) and (adjusted_high_temperature < 45):
            temperature_factor = (adjusted_low_temperature / 5) - 1.1
        # rule 2d: ALT is greater than 15 and AHT is less than 30; use formula (AHT - ALT) / 5
        elif (adjusted_low_temperature > 15) and (adjusted_high_temperature < 30):
            temperature_factor = (
                (adjusted_high_temperature - adjusted_low_temperature) / 5)
        # all other cases; temperature factor is 0
        else:
            temperature_factor = 0
        # final temperature factor
        # if initial temperature is negative then add 1 to the temperature factor if there is:
        if temperature_factor < 0:
            # cover available
            if cover_available == True:
                temperature_factor += 1
            # wind speed is greater than 3 or less than 10
            elif wind_speed > 3 or wind_speed < 10:
                temperature_factor += 1
            # cloud cover is greater than 4
            elif cloud_cover > 4:
                temperature_factor += 1
        return temperature_factor

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        chance_of_rain = self._prediction_model.chance_of_rain()
        outdoors = self._event.get_outdoors()
        cover_available = self._event.get_cover_available()
        wind_speed = self._prediction_model.wind_speed()
        rain_factor = 0
        # calculate initial rain factor
        # rule 1a: if COR less than 20%; use formula COR / -5 + 4
        if chance_of_rain < 20:
            rain_factor = chance_of_rain / -5 + 4
        # rule 1b: if COR greater than 50%; use formula COR / -20 + 1
        elif chance_of_rain > 50:
            rain_factor = chance_of_rain / -20 + 1
        # all other cases
        else:
            rain_factor = 0
        # calculate final rain factor
        # If event is outdoors and cover is available and wind speed is less than 5, then add 1 to RF
        if outdoors == True and cover_available == True and wind_speed < 5:
            rain_factor = rain_factor + 1
        # If rain factors is less than 2 and wind speed is greater than 15; use formula (rain factor + (wind speed / -15))
        elif rain_factor < 2 and wind_speed > 15:
            (rain_factor + (wind_speed/-15))
            # if rain factor less than -9 -> set to -9
            if rain_factor < -9:
                rain_factor = -9
        return rain_factor

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # calculate final temperature = rain factor + temp factor
        final_temperature_factor = self._rain_factor() + self._temperature_factor()
        # if final temp factor less than -5 -> set to -5
        if final_temperature_factor < -5:
            final_temperature_factor = -5

        return final_temperature_factor


class UserInteraction(object):
    """Simple textual interface to drive program."""

    NAME_QUESTION = ("What is the name of the event?")

    OUTDOORS_QUESTION = ("Is the event outdoors?")

    SHELTER_QUESTION = ("Is there covered shelter?")

    TIME_QUESTION = ("What time is the event?")

    PREDICTION_MODEL_QUESTION = ("Select the weather prediction model you wish to use:", [
        "Yesterday's weather.", "Simple prediction.", "Sophisticated prediction."])

    CHECK_AGAIN_QUESTION = [
        ('check', "Would you like to check again?", 'string_boolean')]

    EVENT_QUESTIONS = [
        ('name', NAME_QUESTION, 'string'),
        ('outdoors', OUTDOORS_QUESTION, 'string_boolean'),
        ('shelter', SHELTER_QUESTION, 'string_boolean'),
        ('time', TIME_QUESTION, 'integer')
    ]

    PREDICTION_QUESTION = [
        ('prediction model', PREDICTION_MODEL_QUESTION, 'numeric_option'),
    ]

    N_DAYS_QUESTION = (
        "Enter how many days of data you wish to use for making the prediction:")

    def __init__(self):
        """
        Initialises UserInteraction class.

        Parameters:

        """
        self._event = None
        self._prediction_model = None
        self._n_days = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        responses = {}

        for key, (self.question), type_ in self.EVENT_QUESTIONS:
            if type_ == 'string':
                responses[key] = self.ask_question_string(self.question)
            elif type_ == 'integer':
                responses[key] = self.ask_question_integer(self.question)
            elif type_ == 'string_boolean':
                responses[key] = self.ask_question_string_boolean(
                    self.question)
            else:
                raise ValueError(f"Unknown question type: {type_}")
            print(end='')
        new_event = Event(responses['name'], responses['outdoors'],
                          responses['shelter'], responses['time'])
        self._event = new_event
        return self._event

    def ask_question_string(self, question):
        """Asks a question expecting any string

        Parameters:
            question (str): Text of the question to be displayed.

        Return:
            (input) String typed by user
        """
        print(question, end=' ')
        return input()

    def ask_question_integer(self, question):
        """Asks a question expecting an integer.

        Parameters:
            question (str): Text of the question to be displayed.

        Return:
            (input) Int typed by the user
        """
        while True:
            try:
                print(question, end=' ')
                user_input = int(input())
                if isinstance(user_input, int) and user_input >= 0 and user_input <= 23:
                    return user_input
            except (ValueError):
                pass
            print(
                f"\nError: {user_input} is not an integer value or between 0 and 23. Try again.\n")

    def ask_question_string_boolean(self, question):
        """Asks a question expecting casefold Yes, Y, No or N.

        Parameters:
            question (str): Text of the question to be displayed

        Return:
            (input) Specific string typed by the user (Yes/No, Y/N).casefold
        """
        while True:
            try:
                print(question, end=' ')
                user_input = input().casefold()
                accepted_user_inputs = {
                    'yes', 'y', 'no', 'n'}
                if user_input in accepted_user_inputs:
                    if user_input == "yes" or user_input == "y":
                        return True
                    if user_input == "no" or user_input == "n":
                        return False
            except (ValueError):
                pass
            print(
                f"\nError: {user_input} is not in the form Yes/No or Y/N. Try again.\n")

    def ask_question_numeric_option(self, question, options):
        """Asks a question with a list of answer options, handling invalid input.

        Parameters:
            question (str): Text of the question to be displayed
            options (list[str]): List of answer options

        Return:
            (input) Numeric option entered by user
        """
        while True:
            print(question)
            for key, option in enumerate(options, start=1):
                print(f"  {key}) {option}")
            response = input(f"> ")
            try:
                response = int(response)
                if 1 <= response <= len(options):
                    return options[response - 1]
            except (ValueError, IndexError):
                pass
            print(f"n\nError: {response} is not a valid option. Try again.\n")

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        responses = {}

        for key, (self.question, self.options), type_ in self.PREDICTION_QUESTION:
            if type_ == "numeric_option":
                responses[key] = self.ask_question_numeric_option(
                    self.question, self.options)
            else:
                raise ValueError(f"Unknown question type: {type_}")
        print()
        # Error handling can be added to this method.
        if responses["prediction model"].casefold() == "yesterday's weather.":
            self._prediction_model = YesterdaysWeather(weather_data)
        elif responses["prediction model"].casefold() == "simple prediction.":
            print(self.N_DAYS_QUESTION, end=" ")
            self._n_days = int(input())
            self._prediction_model = SimplePrediction(
                weather_data, self._n_days)
        elif responses["prediction model"].casefold() == "sophisticated prediction.":
            print(self.N_DAYS_QUESTION, end=" ")
            self._n_days = int(input())
            self._prediction_model = SophisticatedPrediction(
                weather_data, self._n_days)
        else:
            raise IndexError(f"Error: Incorrect response. Try again.")

        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # The following print statement is an example of printing out the
        # class name of an object, which you may use for making the
        # advisability output more meaningful.
        print("Based on", type(self._prediction_model).__name__,
              "model, the advisability of holding", self._event, "is", impact)

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        responses = {}
        for key, (self.question), type_ in self.CHECK_AGAIN_QUESTION:
            if type_ == "string_boolean":
                responses[key] = self.ask_question_string_boolean(
                    self.question)
            else:
                raise ValueError(f"Unknown type: {type_}")
        print()
        user_response = responses["check"]
        if user_response.casefold() == "yes" or user_response.casefold() == "y":
            return True
        elif user_response.casefold() == "no" or user_response.casefold() == "n":
            return False


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
