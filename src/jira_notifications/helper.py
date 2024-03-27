import yaml
import datetime
import logging
class Helper:
    """
    Helper class for loading configuration and checking time equality.

    This class provides methods for loading a configuration file and checking if a given time is equal to the current time.

    Attributes:
        config_file (str): The path to the configuration file.

    Methods:
        load_config(): Loads the configuration file and returns the parsed configuration.
        is_time_equal_to_input(daily_toast_time): Checks if the given time is equal to the current time.

    """
    def __init__(self, logger: logging) -> None:
        self.logger = logger

    def load_config(self, config_file):
        """
        This class provides methods for loading a configuration file and checking if a given time is equal to the current time.

        Attributes:
            config_file (str): The path to the configuration file.

        Methods:
            load_config(): Loads the configuration file and returns the parsed configuration.
            is_time_equal_to_inputs(daily_toast_time): Checks if the given time is equal to the current time.
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config
        except FileNotFoundError:
            self.logger.error("Config file not found.")
            return {}

    def is_time_equal_to_input(self, daily_toast_time):
        """
        Checks if the given time is equal to the current time.
        Parameters:
            daily_toast_time (str): The time to compare with the current time in the format "HH:MM".

        Returns:
            bool: True if the given time is equal to the current time, False otherwise.
        :no-index:
        """
        current_time = datetime.datetime.now().strftime("%H:%M")
        if daily_toast_time  == str(current_time):
            return True
        else:
            return False

    def generate_sample_config(self, config_file):
        """Generate a sample config.yaml file"""
        sample_config = {
            'project_names': ['PRA', 'PRB', 'PRC'],
            'users': [],
            'jira_api_url': 'https://jira.example.com',
            'jira_api_token': 'YOUR_API_TOKEN',
            'daily_toast_time': '17:00',
            'tickets_from_last_min': 15,
            'toast_time_seconds': 600,
            'toast_sound': True
        }

        with open(config_file, 'w', encoding='utf-8') as file:
            yaml.dump(sample_config, file, default_flow_style=False)