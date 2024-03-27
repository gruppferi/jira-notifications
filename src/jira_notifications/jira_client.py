from datetime import datetime, timedelta
from jira import JIRA
import logging
import html
class Jira:
    """
    The Jira class provides methods to interact with the Jira API and retrieve information about tickets.

    Attributes:
        config (dict): A dictionary containing the configuration parameters for the Jira instance.
        project_names (list): A list of project names to filter the tickets.
        jira_api_url (str): The URL of the Jira API.
        jira_api_token (str): The API token for authentication.
        tickets_from_last_min (int): The number of minutes to consider when retrieving tickets created in the last X minutes.
        jira_client (JIRA): An instance of the JIRA class from the 'jira' module.

    Methods:
        get_tickets_created_today(): Retrieves the tickets created today.
        get_tickets_created_seconds(): Retrieves the tickets created in the last X minutes.
        prepare_tickets_with_link(tickets, base_url): Prepares the ticket information with hyperlinks.

    """
    def __init__(self, config, logger: logging):
        self.logger = logger
        self.config = config
        self.project_names = self.config.get('project_names', [])
        self.jira_api_url = self.config.get('jira_api_url', '')
        self.jira_api_token = self.config.get('jira_api_token', '')
        self.tickets_from_last_min = self.config.get('tickets_from_last_min', 5)
        options = {
            'server': self.jira_api_url,
            'headers': {
                'Authorization': f'Bearer {self.jira_api_token}'
            }
        }
        self.jira_client = JIRA(options)

    def get_tickets_created_today(self):
        """
        Retrieves the tickets created today.

        Returns:
            list: A list of ticket keys for the tickets created today.

        Raises:
            Exception: If there is an error retrieving the tickets.

        """
        today = datetime.now()
        if "users" in self.config and self.config.get("users"):
            user_queries = [f'(assignee="{user}" OR reporter="{user}")' for user in self.config.get("users")]
            jql = f'project in ({", ".join(self.project_names)}) AND created >= "{today.strftime("%Y-%m-%d")}" AND {" OR ".join(user_queries)}'
        else:
            jql = f'project in ({", ".join(self.project_names)}) AND created >= "{today.strftime("%Y-%m-%d")}"'
        jql += ' ORDER BY created DESC'

        try:
            issues = self.jira_client.search_issues(jql, maxResults=False)
            return [issue.key for issue in issues]
        except Exception as e:
            self.logger.error("Error retrieving tickets:", e)
            return []

    def get_tickets_created_seconds(self):
        """
        Retrieves the tickets created in the last X minutes.

        Returns:
            list: A list of ticket keys for the tickets created in the last X minutes.

        Raises:
            Exception: If there is an error retrieving the tickets.

        """
        today = datetime.now()
        time_window_start = today - timedelta(minutes=self.tickets_from_last_min)
        user_queries = [f'(assignee="{user}" OR reporter="{user}")' for user in self.config.get("users", [])]
        jql = f'project in ({", ".join(self.project_names)}) AND created >= "{time_window_start.strftime("%Y-%m-%d %H:%M")}"'
        if user_queries:
            jql += f' AND {" OR ".join(user_queries)}'
        jql += ' ORDER BY created DESC'

        issues = self.jira_client.search_issues(jql, maxResults=False)
        return [issue.key for issue in issues]

    def prepare_tickets_with_link(self, tickets, base_url):
        """
        Prepare the tickets with links for notification body.

        Args:
            tickets (list): List of tickets.
            base_url (str): Base URL for ticket links.

        Returns:
            str: Notification body with ticket links.
        """
        if tickets is None:
            return ""

        notification_body = ""
        if base_url:
            for ticket in tickets:
                ticket_link = f"<a href='{base_url}/browse/{html.escape(ticket)}'>{html.escape(ticket)}</a>"
                notification_body += f"{ticket_link}\n"
        else:
            for ticket in tickets:
                notification_body += f"{ticket}\n"
        return notification_body

    def prepare_tickets_with_link_windows(self,tickets):
        """
        Prepare the tickets with line breaks for Windows notification body.

        Args:
            tickets (list): A list of ticket keys.

        Returns:
            str: A string with ticket keys separated by line breaks.

        """
        message = "\n".join(tickets)
        return message
