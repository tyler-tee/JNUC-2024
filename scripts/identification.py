import json
from helpers.jamf_client import JamfClient
from helpers.airtable_client import AirtableAPI  # Ensure AirtableAPI is properly imported


def main():
    username = 'example_username'
    password = 'example_password'
    base_url = 'your.jamf.instance.com'

    jamf = JamfClient(username, password, base_url, verify_cert=True)
    airtable = AirtableAPI(api_key='your_airtable_api_key', base_id='your_airtable_base_id')

    if jamf.authenticate():
        print("Authentication successful!")
    else:
        print("Authentication failed, check credentials or network settings.")
        return

    computer_group_id = 999
    computer_group = jamf.get_computer_group(id=computer_group_id)

    if 'Error' in computer_group:
        print(f"Failed to retrieve computer group: {computer_group['Error']}")
        return

    all_computer_details = []

    for computer in computer_group.get('computers', []):
        inventory_details = jamf.get_computer_inventory_details(computer['id'])
        if inventory_details['success']:
            computer_data = {
                'jamf_id': computer['id'],
                'asset_serial': inventory_details['data']['serialNumber'],
                'asset_name': inventory_details['data']['name'],
                'asset_model': inventory_details['data']['model'],
                'user_name': inventory_details['data'].get('userName'),
                'user_email': inventory_details['data'].get('userEmail')
            }

            # Create Airtable record
            airtable_record = airtable.create_record(computer_data)  # Assuming you have a "create_record" method
            if 'id' in airtable_record:
                computer_data['airtable_record_id'] = airtable_record['id']
                print(f"Airtable record created for computer ID {computer['id']}")
            else:
                print(f"Failed to create Airtable record for computer ID {computer['id']}")

            all_computer_details.append(computer_data)
        else:
            print(f"Failed to retrieve inventory for computer ID {computer['id']}: {inventory_details['message']}")

    # Write updated computer details to a JSON file
    with open('identification.json', 'w') as f:
        json.dump(all_computer_details, f, indent=4)

    return all_computer_details


if __name__ == "__main__":
    main()
