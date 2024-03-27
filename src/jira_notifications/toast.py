import os
import platform

if platform.system() == 'Windows' and platform.release() in ("11", "10"):
    from win11toast import toast
else:
    from notifypy import Notify

class Toast:
    """
    A class that represents a toast notification.

    Attributes:
    - icon_path (str): The path to the icon used for the notification.
    - current_notification (Notification): The current notification being displayed.

    Methods:
    - __init__(): Initializes the Toast object.
    - notify(notification_title, notification_body): Displays a notification with the given title and body.
    - close_current_notification(): Closes the current notification.
    - close(): Closes the notification system.

    Example:
        toast = Toast()
        toast.notify("New Message", "You have a new message!")
    """
    def __init__(self, logger):
        self.logger = logger
        self.icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'jira.png'))
        self.sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'jira.wav'))
        self.current_notification = None

    def notify(self, notification_title, notification_body, base_url, sound=False):
        """
        Displays a notification with the given title and body.

        Parameters:
        - notification_title (str): The title of the notification.
        - notification_body (str): The body of the notification.

        Returns:
        None

        Example:
            toast = Toast()
            toast.notify("New Message", "You have a new message!")
        """
        if platform.system() == 'Windows' and platform.release() in ("11", "10"):
            if sound:
                toast(notification_body, audio=self.sound_path, on_click=base_url)
            else:
                toast(notification_body, on_click=base_url)
        else:
            notification = Notify(default_notification_application_name='Jira Notifier Bird')
            notification.title = notification_title
            notification.message = notification_body
            notification.icon = self.icon_path
            if sound:
                notification.audio = self.sound_path
            notification.send()