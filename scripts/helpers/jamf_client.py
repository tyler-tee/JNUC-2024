import requests
from typing import Any, List, Dict


class JamfClient:

    def __init__(self, username: str,
                 password: str,
                 base_url: str,
                 verify_cert: bool = True):

        self.base_url = f'https://{base_url}/api'
        self.base_url_classic = f'https://{base_url}/JSSResource'
        self.username = username
        self.password = password
        self.session = requests.session()
        self.session.headers = {'Accept': 'application/json'}
        self.session.verify = verify_cert

    def authenticate(self) -> str:
        """
        Authenticate to Jamf Pro API using id and secret supplied on instantiation.
        """

        response = self.session.post(f'{self.base_url}/v1/auth/token',
                                     auth=(self.username, self.password))

        if response.status_code == 200:
            self.session.headers['Authorization'] = f'Bearer {response.json()["token"]}'
            return True
        else:
            print('Authentication failed!')
            return False

    def authenticate_api_client(self) -> str:
        """
        Authenticate to Jamf Pro API using id and secret supplied on instantiation.
        """

        payload = {
                "client_id": self.username,
                "client_secret": self.password,
                "grant_type": "client_credentials"
                }

        response = self.session.post(f'{self.base_url}/oauth/token',
                                     json=payload)

        if response.status_code == 200:
            self.session.headers['Authorization'] = f'Bearer {response.json()["access_token"]}'
            return True
        else:
            print('Authentication failed!')
            return False

    def get_all_app_installers(self):
        """
        Retrieve a full List of App Installers from the Jamf Pro Catalog.
        """

        response = self.session.get(f'{self.base_url}/v1/app-installers/titles',
                                    json={'page-size': 999})

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving App Installers", response.status_code, response.content)

    def get_deployed_app_installers(self):
        """
        Retrieve a full List of currently-deployed App Installers.
        """

        response = self.session.get(f'{self.base_url}/v1/app-installers/deployments', json={'page-size': 999})

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving deployed App Installers", response.status_code, response.content)

    def get_app_installer_details(self, app_installer_id: str):
        """
        Retrieve details for a single App Installer.
        """

        response = self.session.get(f'{self.base_url}/v1/app-installers/titles/{app_installer_id}')

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving App Installers",
                  response.status_code,
                  response.content)

    def get_deployment_details(self, deployment_id: str):
        """
        Retrieve details for a single App Installer deployment.
        """

        deployment_uri = f'/v1/app-installers/deployments/{deployment_id}'

        response = self.session.get(f'{self.base_url}{deployment_uri}')

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving deployments",
                  response.status_code,
                  response.content)

    def get_installation_summary(self, deployment_id: str):
        """
        Retrieve installation summary for a single App Installer deployment.
        """

        deployment_uri = f'/v1/app-installers/deployments/{deployment_id}/installation-summary'

        response = self.session.get(f'{self.base_url}{deployment_uri}')

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving deployments",
                  response.status_code,
                  response.content)

    def get_jamf_systems(self):
        """
        Retrieve systems registered with Jamf Pro.
        """

        response = self.session.get(f'{self.base_url_classic}/computers')

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving Jamf systems",
                  response.status_code,
                  response.content)

    def get_computer_inventory(self, sections: List = None, page_size: int = 100,
                               sort: List = None, filter: str = None) -> List:
        """
        Returns List of computer inventory records.
        """

        page = 0
        params = {'page-size': page_size}
        params['sort'] = ','.join(sort) if sort else None
        params['section'] = sections if sections else None

        response = self.session.get(f'{self.base_url}/v1/computers-inventory',
                                    params=params)

        if response.status_code == 200:
            results = response.json()['results']
            print(len(results))
            total = response.json()['totalCount']
            total_pages = (total//page_size)

            while page != total_pages:
                page += 1
                params['page'] = page
                response = self.session.get(f'{self.base_url}/v1/computers-inventory',
                                            params=params)

                if response.status_code == 200:
                    results += response.json()['results']
                    print(len(results))

                else:
                    print('Failed iteration')
                    return [{'Error': f'Failed iteration - {response.status_code}'}]

            return results

        else:
            print('Failed to retrieve records')
            return [{'Error': f'Failed to retrieve records - {response.status_code}'}]

    def get_computer_inventory_details(self, computer_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed inventory information for a specific computer.

        Args:
        computer_id (str): The unique identifier for the computer.

        Returns:
        dict: API response containing detailed computer inventory or error details.
        """
        endpoint = f'/v1/computers-inventory/detail/{computer_id}'
        response = self.session.get(f'{self.base_url}{endpoint}', headers=self.headers)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred while retrieving computer inventory details.",
                'details': response.text
            }

    def get_computer_group(self, name: str = None, id: int = None):
        """
        Retrieve a Computer Group by name or ID - Must supply one or the other.
        """

        if name:
            uri = f'/name/{name}'
        elif id:
            uri = f'/id/{id}'
        else:
            return None

        response = self.session.get(f'{self.base_url_classic}/computergroups/{uri}')

        if response.status_code == 200:
            return response.json()
        else:
            print('Computer gruop retrieval failed!')
            return {'Error': f'Failed to retrieve computer group - {response.status_code}'}

    def get_computer_groups(self) -> List:
        """
        Return a list of all computer groups.
        """

        response = self.session.get(f'{self.base_url}/v1/computer-groups')

        if response.status_code == 200:
            return response.json()
        else:
            print('Computer group retrieval failed!')
            return {'Error': 'Computer group retrieval failed!'}

    def create_computer_group(self, xml_config: str):
        """
        Create a computer group using supplied XML.
        """

        response = self.session.post(f'{self.base_url_classic}/v1/computer-groups/id/-1',
                                     data=xml_config)

        if response.status_code == 200:
            return response.json()
        else:
            print('Computer group creation failed!')
            return {'Error': 'Computer group creation failed!'}

    def delete_computer(self, computer_id: str) -> bool:
        """
        Delete a computer record from Jamf Pro.

        Args:
        computer_id (str): The unique identifier for the computer.

        Returns:
        bool: True if the computer was successfully deleted, False otherwise.
        """
        response = self.session.delete(f'{self.base_url_classic}/computers/id/{computer_id}')

        if response.status_code == 200:
            print(f"Computer with ID {computer_id} deleted successfully.")
            return True
        else:
            print(f"Failed to delete computer: {response.status_code} - {response.text}")
            return False

    def deploy_app_installer(self, jai_name: str, jai_id: str,
                             smart_group_id: str, notification_interval: int = 24,
                             install_config_profiles: bool = True):
        """
        Configure and deploy an App Installer.
        """

        payload = {
            "name": jai_name,
            "enabled":  True,
            "appTitleId": jai_id,
            "siteId": -1,
            "categoryId": 12,
            "smartGroupId": smart_group_id,
            "deploymentType": "INSTALL_AUTOMATICALLY",
            "notificationSettings": {
                "notificationMessage": None,
                "notificationInterval": notification_interval,
                "deadlineMessage": None,
                "deadline": None
            },
            "installPredefinedConfigProfiles": install_config_profiles
        }

        response = self.session.post(f'{self.base_url}/v1/app-installers/deployments',
                                     json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print('App Installer deployment failed!')
            return {'Error': 'App Installer deployment failed!'}

    def retry_failed_deployment(self, deployment_id: str) -> bool:
        """
        Retry failed App Installer deployments.
        """

        retry_uri = f'/api/v1/app-installers/deployments/{deployment_id}/computers/installation-retry'

        response = self.session.post(f'{self.base_url}{retry_uri}')

        if response.status_code == 200:
            return response.json()

        else:
            print("Error retrieving App Installers",
                  response.status_code,
                  response.content)

    def add_patch_title(self, title_name: str, title_id: str) -> Dict:
        """
        Add a Patch Title to Jamf Pro's Patch Management module
        """

        title_config = f"""
        <patch_software_title>
            <name>{title_name}</name>
            <name_id>{title_id}</name_id>
            <source_id>1</source_id>
            <notifications>
                <web_notification>true</web_notification>
                <email_notification>true</email_notification>
            </notifications>
            <category>
                <id>12</id>
                <name>Automatically Configured</name>
            </category>
        </patch_software_title>
        """

        response = self.session.post(f"{self.base_url_classic}/patchsoftwaretitles/id/-1",
                                     data=title_config)

        return response

    def add_patch_title_dashboard(self, patch_title_id: str) -> Dict:
        """
        Add a Patch Software Title to the Jamf Pro Dashboard.
        """

        uri = f"/v2/patch-software-title-configurations/{patch_title_id}/dashboard"

        response = self.session.post(f"{self.base_url}{uri}")

        if response.status_code == 204:
            return response.json()

        else:
            print("Error retrieving App Installers",
                  response.status_code,
                  response.content)

    def get_computer_by_serial(self, serial_number: str) -> Any:
        """
        Find a computer by its serial number.

        Args:
        serial_number (str): The serial number of the computer.

        Returns:
        dict: API response containing computer details or error details.
        """
        url = f'{self.base_url_classic}/computers/serialnumber/{serial_number}'
        response = self.session.get(url, headers=self.headers)

        if response.status_code == 200:
            computer = response.json()
            return computer.get('computer', None)  # Returns computer object if found
        else:
            print(f"Failed to find computer by serial number: {serial_number}")
            return None

    def erase_device(self, computer_id: str, passcode: str) -> Dict[str, Any]:
        """
        Sends an 'EraseDevice' command to a specified computer using the Classic API.

        Args:
        computer_id (str): The unique identifier for the computer.
        passcode (str): Required passcode for device erase, required for devices like iOS.

        Returns:
        dict: API response containing the result of the erase command or error details.
        """
        # Construct the endpoint for the Classic API
        endpoint = f'/computercommands/command/EraseDevice/passcode/{passcode}/id/{computer_id}'

        # Send the POST request to issue the erase command
        response = self.session.post(f'{self.base_url_classic}{endpoint}')

        # Check for the correct success status code: 201 (Created)
        if response.status_code == 201:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred while sending the erase command.",
                'details': response.text
            }

    def check_mdm_command_status(self, statusuuid: str) -> Dict[str, Any]:
        """
        Checks the status of an MDM command using the Classic API.

        Args:
        statusuuid (str): The unique identifier (UUID) for the command status.

        Returns:
        dict: API response containing the command status or error details.
        """
        # Construct the endpoint for checking the status of the command using the status UUID
        endpoint = f'/computercommands/status/{statusuuid}'

        # Send the GET request to retrieve the MDM command status
        response = self.session.get(f'{self.base_url_classic}{endpoint}')

        # Check for success status code: 200 (OK)
        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': f'Failed to retrieve status for command with UUID {statusuuid}.',
                'details': response.text
            }

    def delete_device(self, computer_id: str) -> Dict[str, Any]:
        """
        Deletes a computer from Jamf Pro using the Classic API.

        Args:
        computer_id (str): The unique identifier for the computer to be deleted.

        Returns:
        dict: API response confirming the deletion or containing error details.
        """
        # Construct the endpoint for deleting the computer
        endpoint = f'/computers/id/{computer_id}'

        # Send the DELETE request to remove the computer
        response = self.session.delete(f'{self.base_url_classic}{endpoint}')

        # Check for success status code: 200 (OK)
        if response.status_code == 200:
            return {'success': True, 'message': f'Computer with ID {computer_id} deleted successfully.'}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': f'Failed to delete computer with ID {computer_id}.',
                'details': response.text
            }
