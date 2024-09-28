import json
from helpers.fedex_client import FedExAPI
from helpers.slack_client import SlackClient


def read_json_file(file_path: str):
    """
    Reads a JSON file and returns its contents as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return {}


def handle_slack_response(slack_response):
    """
    Handle the response received from Slack and generate a FedEx return label if necessary.

    Args:
        slack_response (dict): The response payload from Slack.
    """
    user_response = slack_response['actions'][0]['selected_option']['value']

    if user_response == "send_asset_back":
        print("User wants to send the system back. Generating FedEx return label...")
        fedex_data = generate_fedex_return_label(slack_response['user']['id'])

        if fedex_data:
            update_slack_dm(slack_response, fedex_data)


def generate_fedex_return_label(user_id):
    """
    Generate a FedEx return label for the user who wants to send back the system.

    Args:
        user_id (str): Slack user ID who needs the return label.

    Returns:
        dict: FedEx return information such as tracking number, return label URL, and location.
    """
    api_key = 'YOUR_FEDEX_API_KEY'
    fedex = FedExAPI(api_key=api_key, environment='production')  # Use 'sandbox' for testing

    # Dummy data for FedEx label creation (replace with actual FedEx API call)
    shipment_details = {
        'Recipient': {'Email': f'{user_id}@yourcompany.com'},  # Assuming email format
        'Package': {'Weight': '5 lbs', 'Dimensions': '10x10x10'},
        'Sender': {'Address': 'Company Address'}
    }

    response = fedex.create_shipment(shipment_details)
    if response['success']:
        return {
            'tracking_number': response['tracking_number'],
            'label_url': response['label_url'],
            'fedex_location': "FedEx Office Store #123",
            'location_address': "123 FedEx Lane, City, State, ZIP"
        }
    else:
        print("Failed to create FedEx return label:", response['message'])
        return None


def update_slack_dm(slack_response, fedex_data):
    """
    Updates the original Slack DM with FedEx return information.

    Args:
        slack_response (dict): The response payload from Slack.
        fedex_data (dict): FedEx return information to display in the updated message.
    """
    slack_token = "your-slack-api-token"  # Replace with your Slack API token
    slack = SlackClient(slack_token)

    # New Slack blocks to display FedEx return information
    blocks = [
        {
            "type": "header",
            "block_id": "asset_recovery_header",
            "text": {
                "type": "plain_text",
                "text": "Asset Recovery",
                "emoji": True
            }
        },
        {
            "type": "section",
            "block_id": "asset_recovery_preamble",
            "text": {
                "type": "mrkdwn",
                "text": "Great! Here's your FedEx Return information. Please contact IT if you need further assistance!"
            }
        },
        {
            "type": "section",
            "block_id": "return_information",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Tracking Number:* {fedex_data['tracking_number']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Return Label URL:* {fedex_data['label_url']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*FedEx Location:* {fedex_data['fedex_location']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Location Address:* {fedex_data['location_address']}"
                }
            ]
        }
    ]

    # Use Slack's chat.update API to update the original message
    response_url = slack_response['response_url']
    slack.update_message(response_url, blocks)


def main():
    slack_response = read_json_file('sample_slack_response.json')
    handle_slack_response(slack_response)


if __name__ == "__main__":
    main()
