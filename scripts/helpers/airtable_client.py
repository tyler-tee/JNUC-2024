import requests
import json
from typing import Dict, Any, Optional


class AirtableAPI:
    def __init__(self, api_key: str, base_id: str):
        """
        Initialize the Airtable API client.

        Args:
        api_key (str): API key for authentication with the Airtable API.
        base_id (str): The base ID from which data will be accessed.
        """
        self.api_key = api_key
        self.base_url = f'https://api.airtable.com/v0/{base_id}'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()

    def list_records(self, table_name: str, view: Optional[str] = None, fields: Optional[list] = None,
                     filter_by_formula: Optional[str] = None) -> Dict[str, Any]:
        """
        List records from a specific table in the Airtable base.

        Args:
        table_name (str): The name of the table to retrieve records from.
        view (str, optional): The name of the view in the table to filter records.
        fields (list, optional): A list of field names to return in the results.
        filter_by_formula (str, optional): A formula used to filter records.

        Returns:
        dict: API response containing records or error details.
        """
        params = {}
        if view:
            params['view'] = view
        if fields:
            params['fields'] = fields
        if filter_by_formula:
            params['filterByFormula'] = filter_by_formula

        response = self.session.get(f'{self.base_url}/{table_name}', headers=self.headers, params=params)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred with your Airtable request.",
                'details': response.text
            }

    def get_record(self, table_name: str, record_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific record from a table.

        Args:
        table_name (str): The name of the table from which to retrieve the record.
        record_id (str): The ID of the record to retrieve.

        Returns:
        dict: API response containing the record or error details.
        """
        url = f'{self.base_url}/{table_name}/{record_id}'
        response = self.session.get(url, headers=self.headers)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred while retrieving the record from Airtable.",
                'details': response.text
            }

    def update_record(self, table_name: str, record_id: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific record in a table.

        Args:
        table_name (str): The name of the table containing the record.
        record_id (str): The ID of the record to update.
        fields (dict): Dictionary of field names and their new values to be updated.

        Returns:
        dict: API response containing the updated record or error details.
        """
        url = f'{self.base_url}/{table_name}/{record_id}'
        payload = json.dumps({'fields': fields})
        response = self.session.patch(url, headers=self.headers, data=payload)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred while updating the record in Airtable.",
                'details': response.text
            }

    def delete_record(self, table_name: str, record_id: str) -> Dict[str, Any]:
        """
        Delete a specific record from a table.

        Args:
        table_name (str): The name of the table containing the record.
        record_id (str): The ID of the record to delete.

        Returns:
        dict: API response confirming deletion or providing error details.
        """
        url = f'{self.base_url}/{table_name}/{record_id}'
        response = self.session.delete(url, headers=self.headers)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}
        else:
            return {
                'success': False,
                'status_code': response.status_code,
                'reason': response.reason,
                'message': "An error occurred while deleting the record from Airtable.",
                'details': response.text
            }
