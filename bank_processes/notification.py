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

    def send_notification(self, path: str):
        """Method to send notifications to users via their preferred channels,
         such as email, SMS, push notifications, or in-app messages."""
        notification.notify(
            title=self.status,
            message=self.message,
            timeout=30
        )

        with open(f'notification/{path}.txt', 'a') as file:
            file.write(self.message)
            file.write('\n')

    def forgot_username_notification(self, *, title: str, message: str, channel: str):
        """
        Sends a notification to the user regarding their forgotten username.

        Parameters
        ----------
        title : str
            The title of the notification.
        message : str
            The message content of the notification.
        channel : str
            The Location of the notification

        Notes
        -----
        This function sets the notification title and message, then triggers the sending of the notification.
        """
        # Set the status of the notification with the provided title.
        self.status = title

        # Set the message of the notification with the provided message.
        self.message = message

        # Set the location of the notification with the provided path
        self.deliver_channel = channel

        # Call the method to send the notification.
        self.send_notification(path=self.deliver_channel)

    def schedule_notification(self):
        """Method to schedule notifications for future delivery,
        allowing users to set reminders or receive alerts at specific times or dates."""
        pass

    def bvn_creation(self, *, title: str, message: str):
        """Method to trigger notifications in response to each BVN creation."""
        self.status = title
        self.message = message

        self.send_notification()

    def account_creation(self, *, title: str, message: str):
        """Method to manage notification account creation."""
        self.status = title
        self.message = message

        self.send_notification()

    def sign_in(self, *, title: str, message: str):
        """Method to notify a sign in has been made."""
        self.status = title
        self.message = message

        self.send_notification()

    def forgot_password(self, *, title: str, message:str):
        """Method to handle user forgetting their password, a notification."""
        self.status = title
        self.message = message

        self.send_notification()

    def sign_out(self, *, title: str, message: str):
        """Method to maintain a user signing out notfication."""
        self.status = title
        self.message = message

        self.send_notification()

    def transfer_notification(self, *, title: str, message: str):
        """Method to trigger a transfer notification."""
        self.status = title
        self.message = message

        self.send_notification()

    def withdraw_notification(self, *, title: str, message: str):
        """Method to trigger a withdrawal notification."""
        self.status = title
        self.message = message

        self.send_notification()

    def deposit_notification(self, *, title: str, message: str):
        """Method to trigger a deposit notification."""
        self.status = title
        self.message = message

        self.send_notification()

    def fixed_deposit_creation_notification(self, *, title: str, message: str):
        """Method to trigger a fixed deposit creation notification."""
        self.status = title
        self.message = message

        self.send_notification()

    def fixed_deposit_top_up_notification(self, *, title: str, message: str):
        """Method to trigger a fixed deposit top up notification."""
        self.status = title
        self.message = message

        self.send_notification()
