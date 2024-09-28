import json
from helpers.slack_client import SlackClient


def read_identification_json(file_path: str):
    """
    Reads the 'identification.json' file and extracts user emails and system serial numbers.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list of dict: A list of dictionaries containing emails and serial numbers.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            user_data = [
                {
                    'email': item['userAndLocation']['email'],
                    'serial_number': item['hardware']['serialNumber']
                }
                for item in data
            ]
            return user_data
    except Exception as e:
        print(f"Error reading or parsing JSON file: {e}")
        return []


def send_direct_message(slack_token: str, email: str, serial_number: str):
    """
    Send a direct message to a user's email via Slack with a given system serial number using Slack blocks.

    Args:
        slack_token (str): Authentication token for Slack.
        email (str): User email to send message to.
        serial_number (str): System serial number to include in the message.
    """
    slack = SlackClient(token=slack_token)

    # Slack blocks with the serial number embedded in the message
    blocks = [
            {
                "type": "header",
                "block_id": "asset_recovery_header",
                "text": {
                    "type": "plain_text",
                    "text": "This is a header block",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "asset_recovery_question",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello, our records indicate asset {asset} hasn't checked into Jamf in a while. "
                    "Do you still have this system?"
                }
            },
            {
                "type": "actions",
                "block_id": "asset_recovery_response",
                "elements": [
                    {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "I no longer have this system"
                                },
                                "value": "not_in_possession"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "I want to send this system back"
                                },
                                "value": "send_asset_back"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "I don't recognize this system"
                                },
                                "value": "asset_unrecognized"
                            }
                        ],
                        "action_id": "asset_recovery_initial"
                    }
                ]
            }
        ]

    # Find user ID by email
    user_id = slack.find_user_by_email(email)
    if user_id:
        success = slack.send_message(channel_id=user_id, blocks=blocks)
        if success:
            print(f"Message successfully sent to {email}")
            return True
        else:
            print(f"Failed to send message to {email}")
            return False
    else:
        print(f"Could not find Slack user with email: {email}")
        return False


def main():
    slack_token = 'your-slack-api-token'  # Replace with your actual Slack token
    user_data = read_identification_json('identification.json')

    # Loop through each user and send a direct message
    for user in user_data:
        email = user['email']
        serial_number = user['serial_number']
        send_direct_message(slack_token, email, serial_number)


if __name__ == "__main__":
    main()
