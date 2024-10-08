import time
import os
from helpers.jamf_client import JamfClient


def main():
    # Define your Jamf Pro credentials and base URL
    username = os.getenv('JAMF_USERNAME', 'your_username')
    password = os.getenv('JAMF_PASSWORD', 'your_password')
    base_url = os.getenv('JAMF_BASE_URL', 'yourServer.jamfcloud.com')

    # Device serial number and passcode, fetched from environment variables
    serial_number = os.getenv('DEVICE_SERIAL_NUMBER', 'your_device_serial')
    passcode = os.getenv('DEVICE_PASSCODE', 'your_device_passcode')

    # Ensure serial_number and passcode are set
    if not serial_number or not passcode:
        print("Error: Serial number and passcode must be provided.")
        return

    # Instantiate the JamfClient
    jamf_client = JamfClient(username=username, password=password, base_url=base_url)

    # Authenticate the JamfClient
    if not jamf_client.authenticate():
        print("Failed to authenticate. Exiting.")
        return

    # Step 1: Find the computer by serial number
    computer = jamf_client.find_asset_by_serial(serial_number)

    if not computer:
        print(f"Computer with serial number {serial_number} not found.")
        return

    computer_id = computer['id']
    print(f"Found computer with ID: {computer_id}")

    # Step 2: Send the EraseDevice command to the computer
    erase_response = jamf_client.erase_device(computer_id, passcode)

    if not erase_response['success']:
        print(f"Failed to send EraseDevice command: {erase_response['message']}")
        return

    # Retrieve the status UUID from the response
    status_uuid = erase_response['data']['computer_command']['command']['command_uuid']
    print(f"EraseDevice command sent successfully. Status UUID: {status_uuid}")

    # Step 3: Loop and wait for the command to be 'Acknowledged'
    print("Waiting for the EraseDevice command to be acknowledged...")

    check_counter = 0
    while check_counter < 10:
        check_counter += 1
        status_response = jamf_client.check_mdm_command_status(status_uuid)

        if status_response['success']:
            status = status_response['data']['computer_command']['status']
            print(f"Current status: {status}")

            if status == 'Acknowledged':
                print(f"Command acknowledged for computer ID: {computer_id}")
                break
        else:
            print(f"Failed to check command status: {status_response['message']}")
            return

        # Wait for a minute before checking again
        time.sleep(60)

    # Step 4: Delete the computer from Jamf Pro
    delete_response = jamf_client.delete_device(computer_id)

    if delete_response['success']:
        print(f"Computer with ID {computer_id} deleted successfully.")
    else:
        print(f"Failed to delete computer: {delete_response['message']}")


if __name__ == "__main__":
    main()
