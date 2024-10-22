import requests
from typing import List


class SlackClient:

    def __init__(self, token: str,
                 verify_cert: bool = True):

        self.base_url = "https://slack.com/api"
        self.session = requests.session()
        self.session.headers = {"Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"}
        self.session.verify = verify_cert

    def send_message(self, channel_id: str, attachments: List = None, text: str = None, blocks: List = None) -> bool:
        """
        Post a message to a Slack channel or user.

        Args:
            channel_id (str): The ID of the Slack channel or user to send the message to.
            attachments (list, optional): Optional attachments for the message.
            text (str, optional): Optional plain text for the message.
            blocks (list, optional): Optional Slack block elements for rich messaging.

        Returns:
            bool: True if the message was successfully sent, False otherwise.
        """
        payload = {"channel": channel_id}

        if blocks:
            payload["blocks"] = blocks
        elif text:
            payload["text"] = text
        elif attachments:
            payload["attachments"] = attachments
        else:
            print("Slack Error: Must provide text, attachments, or blocks to send a message.")
            return False

        response = self.session.post(f"{self.base_url}/chat.postMessage", json=payload)

        if response.status_code == 200 and response.json()['ok']:
            return True
        else:
            print("Slack Error: ", response.status_code, response.json())
            return False

    def update_message(self, response_url: str, blocks: list) -> bool:
        """
        Update an existing message in Slack with new blocks.

        Args:
            response_url (str): The URL to update the message.
            blocks (list): The updated message blocks.

        Returns:
            bool: True if the message was successfully updated, False otherwise.
        """
        payload = {"blocks": blocks}

        response = self.session.post(response_url, json=payload)

        if response.status_code == 200 and response.json()['ok']:
            return True
        else:
            print("Slack Error:", response.status_code, response.json())
            return False

    def find_user_by_email(self, email: str) -> str:
        """
        Find a Slack user ID associated with an email address.

        Args:
            email (str): The email address of the user to find.

        Returns:
            str: The Slack user ID associated with the email address, or None if not found.
        """
        url = f"{self.base_url}/users.lookupByEmail"
        params = {"email": email}
        response = self.session.get(url, params=params)

        if response.status_code == 200 and response.json()['ok']:
            user_id = response.json()['user']['id']
            return user_id
        else:
            print(f"Failed to find user by email {email}: {response.status_code}, {response.json()}")
            return None
