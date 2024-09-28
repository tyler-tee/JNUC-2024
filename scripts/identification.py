import json
from helpers.jamf_client import JamfClient


def identification():
    # Example credentials (replace with actual credentials for real use)
    username = 'example_username'
    password = 'example_password'
    base_url = 'your.jamf.instance.com'  # Replace with your actual Jamf instance URL

    # Create an instance of the JamfClient
    jamf = JamfClient(username=username,
                      password=password,
                      base_url=base_url,
                      verify_cert=True)  # Set to False if you have SSL certificate issues

    # Authenticate to the API
    if jamf.authenticate():
        print("Authentication successful!")
    else:
        print("Authentication failed, check credentials or network settings.")
        return

    # ID of the computer group to retrieve systems from
    computer_group_id = 999

    # Retrieve the systems from the specified computer group
    computer_group = jamf.get_computer_group(id=computer_group_id)

    if 'Error' in computer_group:
        print(f"Failed to retrieve computer group: {computer_group['Error']}")
        return

    # List to hold inventory details for each computer
    all_computer_details = []

    # Iterate through each computer in the computer group
    for computer in computer_group.get('computers', []):  # Ensure 'computers' key exists and is iterable
        inventory_details = jamf.get_computer_inventory_details(computer['id'])
        if inventory_details['success']:
            all_computer_details.append(inventory_details['data'])
            print(f"Retrieved inventory for computer ID {computer['id']}")
        else:
            print(f"Failed to retrieve inventory for computer ID {computer['id']}: {inventory_details['message']}")

    with open('identification.json', 'w') as f:
        f.write(json.dumps(all_computer_details, indent=4))

    return all_computer_details


if __name__ == "__main__":
    identification()
