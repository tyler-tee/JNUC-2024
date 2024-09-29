# JNUC-2024

This repository is setup to host companion content for the **JNUC 2024** session _"Asset Recovery in a Remote World"_. The session covers strategies and technologies for reclaiming distributed assets in a remote work environment, focusing on streamlining the process through automation and integration with various platforms.


## Repository Structure

- `scripts/`
  - `identification.py` - Script to identify and prepare user data for communication.
  - `communication.py` - Script for sending notifications to users via Slack to check the status of their assets.
  - `reclamation.py` - Script for processing user responses and generating FedEx return labels if necessary.
  - `sample_slack_response.json` - Sample JSON file that mimics a response from Slack's interactive components.
- `helpers/`
  - `airtable_client.py` - Client module for interacting with Airtable API.
  - `fedex_client.py` - Client module for interacting with FedEx API to generate return labels.
  - `jamf_client.py` - Client module for interacting with Jamf API to manage and retrieve system data.
  - `slack_client.py` - Client module for handling communication with Slack users via the Slack API.

## Setup

### Prerequisites

- Python 3.6 or higher.
- `requests` library installed.

## Configuration

You must configure your API credentials prior to use:

1. [Airtable](https://airtable.com/developers/web/api/authentication)
2. [FedEx](https://developer.fedex.com/api/en-us/get-started.html)
3. [Jamf Pro](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/API_Roles_and_Clients.html?utm_source=google&utm_medium=cpc&utm_content=17810239897_141711808040_jamf+api_p_c_g_705452156101&gad_source=1&gclid=CjwKCAjw9eO3BhBNEiwAoc0-jVldawpm0NOtGpSciB0uQbhxz6XKlZT9kiF0ei1cWfk7cjCyS13ZnBoCo_wQAvD_BwE)
4. [Slack](https://www.lambdasandlapdogs.com/blog/building-slack-apps-with-tines-part-1)

## Alternate Libraries

- Airtable
  - [PyAirtable](https://github.com/gtalarico/pyairtable)
- Jamf Pro
  - [Python SDK](https://github.com/macadmins/jamf-pro-sdk-python)
  - [Go SDK](https://github.com/deploymenttheory/go-api-sdk-jamfpro)
- Slack
  - [Python SDK](https://github.com/slackapi/python-slack-sdk)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
