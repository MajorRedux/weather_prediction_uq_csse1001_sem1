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
from prediction import WeatherPrediction, YesterdaysWeather
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
        return 'Event({0} @ {1},{2},{3})'.format(self._name, self._time, self._outdoors, self._cover_available)


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
        high_temperature = None
        low_temperature = None
        temperature_factor = None
        time = None
        outdoors = None
        adjusted_high_temperature = None
        adjusted_low_temperature = None

        temperature_factor = 0
        # adjusted_humidity =
        adjusted_high_temperature = self._humidity_adjustment()
        adjusted_low_temperature = self._humidity_adjustment()
        # initial temperature factor
        if (((time >= 6 and time <= 19) and outdoors and (adjusted_high_temperature >= 30)) or (adjusted_high_temperature <= 45):
            temperature_factor=(adjusted_high_temperature / -5) + 6
        elif ((time >= 0 and time <= 5) or (time >= 20 and time <= 23)) and (adjusted_low_temperature < 5) and (adjusted_high_temperature < 45):
            temperature_factor=(adjusted_low_temperature / 5) - 1.1
        elif (adjusted_low_temperature > 15) and (adjusted_high_temperature < 30):
            temperature_factor=(
                (adjusted_high_temperature - adjusted_low_temperature) / 5)
        else:
            temperature_factor=0
        # final temperature factor

        return temperature_factor

    def _humidity_adjustment(self, temperature):
        """
        Adjusts predicted temperature based on humidity, high or low temperatures.

        Parameters:
            humidity(int): Humidity as an int representing percentage
            temperature(float): Adjusted temperature

        Return:
            adjusted_humidity_temperature(float): temperature after humidity adjustment
        """

        humidity_factor=0
        adjusted_humidity_temperature=0
        if humidity > 70:
            humidity_factor=humidity/20
            if temperature > 0:
                return adjusted_humidity_temperature + humidity_factor
            elif temperature < 0:
                return adjusted_humidity_temperature - humidity_factor
            else:
                raise ValueError(f"Unknown temperature value.")

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        return rain_factor

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """


        raise NotImplementedError


class UserInteraction(object):
    """Simple textual interface to drive program."""

    NAME_QUESTION=("What is the name of the event?")

    OUTDOORS_QUESTION=("Is the event outdoors?")

    SHELTER_QUESTION=("Is there covered shelter?")

    TIME_QUESTION=("What time is the event?")

    PREDICTION_MODEL_QUESTION=("Select the weather prediction model you wish to use:", [
                                 "Yesterday's weather.", "Simple prediction.", "Sophisticated prediction."])

    CHECK_AGAIN_QUESTION=[
        ('check', "Would you like to check again?", 'string_boolean')]

    EVENT_QUESTIONS=[
        ('name', NAME_QUESTION, 'string'),
        ('outdoors', OUTDOORS_QUESTION, 'string_boolean'),
        ('shelter', SHELTER_QUESTION, 'string_boolean'),
        ('time', TIME_QUESTION, 'integer')
    ]

    PREDICTION_QUESTION=[
        ('prediction model', PREDICTION_MODEL_QUESTION, 'numeric_option'),
    ]

    def __init__(self):
        """
        """
        self._event=None
        self._prediction_model=None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        responses={}

        for key, (self.question), type_ in self.EVENT_QUESTIONS:
            if type_ == 'string':
                responses[key]=self.ask_question_string(self.question)
            elif type_ == 'integer':
                responses[key]=self.ask_question_integer(self.question)
            elif type_ == 'string_boolean':
                responses[key]=self.ask_question_string_boolean(
                    self.question)
            else:
                raise ValueError(f"Unknown question type: {type_}")
            print(end='')
        new_event=Event(responses['name'], responses['outdoors'],
                          responses['shelter'], responses['time'])
        self._event=new_event
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
                user_input=int(input())
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
                user_input=input().casefold()
                accepted_user_inputs={
                    'yes', 'y', 'no', 'n'}
                if user_input in accepted_user_inputs:
                    return user_input
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
            response=input("> ")
            try:
                response=int(response)
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
        responses={}

        for key, (self.question, self.options), type_ in self.PREDICTION_QUESTION:
            if type_ == "numeric_option":
                responses[key]=self.ask_question_numeric_option(
                    self.question, self.options)
            else:
                raise ValueError(f"Unknown question type: {type_}")
        print()
        # Error handling can be added to this method.
        if responses["prediction model"].casefold() == "yesterday's weather.":
            self._prediction_model=YesterdaysWeather(weather_data)
        elif responses["prediction model"].casefold() == "simple prediction.":
            self._prediction_model=YesterdaysWeather(weather_data)
        elif responses["prediction model"].casefold() == "sophisticated prediction.":
            self._prediction_model=YesterdaysWeather(weather_data)
        else:
            raise IndexError(f"Error: Incorrect response. Try again.")

        # Cater for other prediction models when they are implemented.
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
        responses={}
        for key, (self.question), type_ in self.CHECK_AGAIN_QUESTION:
            if type_ == "string boolean":
                responses[key]=self.ask_question_string_boolean(
                    self.question)
            else:
                raise ValueError(f"Unknown type: {type_}")
        print()
        user_response=responses["check"]
        if user_response.casefold() == "yes" or "y":
            return True
        else:
            return False


def main():
    """Main application's starting point."""
    check_again=True
    weather_data=WeatherData()
    weather_data.load("weather_data.csv")
    user_interface=UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event=user_interface.get_event_details()

    while check_again:
        prediction_model=user_interface.get_prediction_model(weather_data)
        decision=EventDecision(event, prediction_model)
        impact=decision.advisability()
        user_interface.output_advisability(impact)
        check_again=user_interface.another_check()


if __name__ == "__main__":
    main()
