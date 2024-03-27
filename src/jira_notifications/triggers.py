from jira_notifications.jira_client import Jira
from jira_notifications.toast import Toast
from jira_notifications.helper import Helper
import platform

class Triggers:
    """
    A class that represents triggers for Jira notifications.

    Attributes:
    - config (dict): The configuration for the triggers.
    - jira_client (Jira): An instance of the Jira class for interacting with the Jira API.
    - toast (Toast): An instance of the Toast class for displaying notifications.
    - helper (Helper): An instance of the Helper class for loading configuration and checking time equality.

    Methods:
    - __init__(config): Initializes the Triggers object with the given configuration.
    - jira_daily_toast(repeated): Checks if it is the specified time for daily notifications and displays Jira tickets created today.
    - jira_routine_toast(): Displays Jira tickets created in the last specified minutes.

    Example:
        config = {
            "daily_toast_time": "09:00",
            "jira_api_url": "https://example.com",
            "project_names": ["Project1", "Project2"],
            "users": ["user1", "user2"],
            "tickets_from_last_min": 5
        }
        triggers = Triggers(config)
        triggers.jira_daily_toast(repeated=False)
        triggers.jira_routine_toast()
    """
    def __init__(self, config, logger) -> None:
        self.config = config
        self.logger = logger
        self.jira_client = Jira(self.config, self.logger)
        self.toast = Toast(self.logger)
        self.helper = Helper(self.logger)

    def jira_daily_toast(self, repeated):
        """
        Checks if it is the specified time for daily notifications and displays Jira tickets created today.

        Parameters:
        - repeated (bool): Indicates whether the notification is repeated or not.

        Returns:
        None

        Example:
        triggers.jira_daily_toast(repeated=False)
        """
        if self.helper.is_time_equal_to_input(self.config.get("daily_toast_time")) and not repeated:
            tickets = self.jira_client.get_tickets_created_today()
            if tickets:
                if platform.system() == 'Windows' and platform.release() in ("11", "10"):
                    link = self.jira_client.prepare_tickets_with_link_windows(tickets)
                else:
                    link = self.jira_client.prepare_tickets_with_link(tickets, self.config.get("jira_api_url"))
                self.toast.notify("Jira Today Notification", link, self.config.get("jira_api_url"), self.config.get("toast_sound"))

    def jira_routine_toast(self):
        """
        Checks for new Jira tickets created in the last specified seconds and displays them.

        Parameters:
        - None

        Returns:
        - None

        Example:
        triggers.jira_routine_toast()
        """
        tickets = self.jira_client.get_tickets_created_seconds()
        if tickets:
            if platform.system() == 'Windows' and platform.release() in ("11", "10"):
                link = self.jira_client.prepare_tickets_with_link_windows(tickets)
            else:
                link = self.jira_client.prepare_tickets_with_link(tickets, self.config.get("jira_api_url"))
            self.toast.notify("Jira New Ticket(S)", link, self.config.get("jira_api_url"), self.config.get("toast_sound"))
