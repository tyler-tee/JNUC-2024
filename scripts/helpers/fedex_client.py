import requests
from typing import Dict, Any, Union


class FedExAPI:
    def __init__(self, api_key: str, environment: str = 'sandbox'):
        """
        Initialize the FedEx API client.

        Args:
        api_key (str): Bearer token for authorization.
        environment (str, optional): Determines the API environment ('sandbox' or 'production').
        """
        self.api_key = api_key
        self.base_url = 'https://apis-sandbox.fedex.com' if environment == 'sandbox' else 'https://apis.fedex.com'
        self.client = requests.session()
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    ERROR_DICT = {
        400: "Bad request. Please check your input.",
        401: "Unauthorized. Check your API key.",
        403: "Forbidden. Your credentials do not allow access to this resource.",
        404: "Requested resource could not be found.",
        500: "Internal Server Error. Please try again later.",
        503: "Service Unavailable. The server is temporarily unable to service your request."
    }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to a specified endpoint.

        Args:
        method (str): HTTP method
        endpoint (str): API endpoint to be appended to the base URL.
        kwargs (dict): Additional arguments to be passed to requests method.

        Returns:
        dict: Response data or error details.
        """
        url = f'{self.base_url}{endpoint}'
        headers = kwargs.pop('headers', {})
        headers.update(self.headers)

        response = self.client.request(method, url, headers=headers, **kwargs)

        if response.status_code == 200:
            return {'success': True, 'data': response.json()}

        error_details = {
            'success': False,
            'status_code': response.status_code,
            'reason': response.reason,
            'message': self.ERROR_DICT.get(response.status_code, "An error occurred with your request."),
            'details': response.text
        }

        return error_details

    def create_shipment(self, requested_shipment: Dict[str, Any], label_response_options: str,
                        account_number: Dict[str, Any], transaction_id: Union[str, None] = None,
                        locale: str = "en_US") -> Dict[str, Any]:
        """
        Create a shipment using the FedEx API.

        Args:
        requested_shipment (dict): Detailed data for shipment.
        label_response_options (str): Options for label response, such as 'URL' or 'INLINE'.
        account_number (dict): FedEx account number details.
        transaction_id (str, optional): Unique identifier for the transaction.
        locale (str, optional): Locale setting, defaults to 'en_US'.

        Returns:
        dict: API response data.
        """
        payload = {
            'requestedShipment': requested_shipment,
            'labelResponseOptions': label_response_options,
            'accountNumber': account_number  # Assuming the account number details are needed as a dict
        }

        headers = {'X-locale': locale}
        if transaction_id:
            headers['x-customer-transaction-id'] = transaction_id

        return self._make_request('POST', '/ship/v1/shipments', json=payload, headers=headers)

    def cancel_shipment(self, shipment_id: str, transaction_id: Union[str, None] = None,
                        locale: str = "en_US") -> Dict[str, Any]:
        """
        Cancel a shipment using the FedEx API.

        Args:
        shipment_id (str): The identifier for the shipment to cancel.
        transaction_id (str, optional): Unique identifier for the transaction.
        locale (str, optional): Locale setting, defaults to 'en_US'.

        Returns:
        dict: API response data.
        """
        endpoint = f'/ship/v1/shipments/{shipment_id}/cancel'
        headers = {'X-locale': locale}
        if transaction_id:
            headers['x-customer-transaction-id'] = transaction_id

        return self._make_request('PUT', endpoint, headers=headers)

    def validate_shipment(self, shipment_details: Dict[str, Any], transaction_id: Union[str, None] = None,
                          locale: str = "en_US") -> Dict[str, Any]:
        """
        Validate shipment details using the FedEx API without creating a shipment.

        Args:
        shipment_details (dict): Detailed data for shipment validation.
        transaction_id (str, optional): Unique identifier for the transaction.
        locale (str, optional): Locale setting, defaults to 'en_US'.

        Returns:
        dict: API response data.
        """
        payload = {
            'shipmentDetails': shipment_details
        }

        headers = {'X-locale': locale}
        if transaction_id:
            headers['x-customer-transaction-id'] = transaction_id

        return self._make_request('POST', '/ship/v1/shipments/validate', json=payload, headers=headers)
