from plyer import notification
# import time, datetime


class Notification:

    def __init__(self, recipient: str = None, message: str = None, timestamp: str = None, notification_type: str = None,
                 delivery_method: str = None, status: str = None, delivery_channel: str = None, priority: str = None,
                 notification_id: str = None,
                 acknowledgement_status: str = None, sender: str = None, attachments: str = None):
        self.recipient = recipient  # The user or users who will receive the notification.
        self.message = message  # The content of the notification to be sent.
        self.timestamp = timestamp  # The timestamp indicating when the notification was generated
        self.notification_type = notification_type  # The type of notification
        self.delivery_method = delivery_method  # The method used to deliver the notification
        self.status = status  # The status of the notification
        self.deliver_channel = delivery_channel  # The specific channel or address used for delivery
        self.priority = priority  # The priority level of the notification
        self.notification_id = notification_id  # A unique identifier for the notification
        self.acknowledgement_status = acknowledgement_status  # Indicating if the notification has been acknowledged.
        self.sender = sender  # The entity or system responsible for sending the notification
        self.attachments = attachments  # Any additional files or media included with the notification

    @classmethod
    def send_notification(cls, title: str, message: str, channel: str):
        """
        Sends a notification to users via their preferred channels and logs the message to a text file.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location (used for logging).

        Notes
        -----
        This method is responsible for sending notifications and appending the message to a log file.
        """
        # Send notification using the appropriate method (e.g., email, SMS, push notification)
        notification.notify(
            title=title,
            message=message,
            timeout=30  # Example: Notification timeout
        )

        # Log the notification message to a text file
        with open(f'notification/{channel}.txt', 'a') as file:
            file.write(message)
            file.write('\n')

    def schedule_notification(self):
        """
        Method to schedule notifications for future delivery.

        Notes
        -----
        This method can be implemented to schedule notifications at specific times or dates.
        """
        pass  # Placeholder for future implementation

    def trigger_notification(self, title: str, message: str, channel: str):
        """
        Helper method to set notification details and trigger sending.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method sets the notification details and then calls `send_notification` to send the notification.
        """
        # Set notification details
        self.status = title
        self.message = message
        self.deliver_channel = channel

        # Send notification using the configured details
        self.send_notification(title, message, channel)

    def forgot_username_notification(self, *, title: str, message: str, channel: str):
        """
        Sends a notification to the user regarding their forgotten username.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for forgotten username scenarios.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def account_creation_notification(self, *, title: str, message: str, channel: str):
        """
        Manages notification for account creation.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for account creation events.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def sign_in_notification(self, *, title: str, message: str, channel: str):
        """
        Notifies a sign-in event.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for user sign-in events.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def forgot_password_notification(self, *, title: str, message: str, channel: str):
        """
        Handles notification for user forgetting their password.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for forgotten password scenarios.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def sign_out_notification(self, *, title: str, message: str, channel: str):
        """
        Maintains a user signing out notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for user sign-out events.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def transfer_notification(self, *, title: str, message: str, channel: str):
        """
        Triggers a transfer notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for transfer transactions.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def withdraw_notification(self, *, title: str, message: str, channel: str):
        """
        Triggers a withdrawal notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for withdrawal transactions.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def deposit_notification(self, *, title: str, message: str, channel: str):
        """
        Triggers a deposit notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for deposit transactions.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def fixed_deposit_creation_notification(self, *, title: str, message: str, channel: str):
        """
        Triggers a fixed deposit creation notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for fixed deposit creation events.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)

    def fixed_deposit_top_up_notification(self, *, title: str, message: str, channel: str):
        """
        Triggers a fixed deposit top-up notification.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The content of the notification message.
        channel : str
            The delivery channel or location.

        Notes
        -----
        This method triggers the notification sending process for fixed deposit top-up events.
        """
        # Trigger the notification with provided details
        self.trigger_notification(title=title, message=message, channel=channel)