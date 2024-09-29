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


## Endpoints of Interest


## Airtable

**GET**  
[/v0/appXXXXXXXXXX/Table](https://airtable.com/developers/web/api/list-records)  
Retrieve records from the specified table.

**Response**

```
{
  "records": [
    {
      "createdTime": "TIMESTAMP",
      "fields": {
        "Address": "123 Main St",
        "Name": "Main Street",
        "Visited": true
      },
      "id": "record_id"
    },
    ...
  ]
}
```

**POST**  
[/v0/appXXXXXXXXXX/Table](https://airtable.com/developers/web/api/create-records)  
Create a new record in the table.

**Response**

```
{
  "records": [
    {
      "createdTime": "TIMESTAMP",
      "fields": {
        "Address": "123 Main St",
        "Name": "Main Street",
        "Visited": true
      },
      "id": "record_id"
    },
    ...
  ]
}
```

## FedEx

**POST**  
[/ship/v1/shipments](https://developer.fedex.com/api/en-us/catalog/ship/v1/docs.html#operation/Create%20Shipment)  
Generate shipping labels for asset returns.

**Response**

```
{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "cancelledTag": true,
    "successMessage": "success"
  }
}
```

**POST**  
[/track/v1/trackingnumbers](https://developer.fedex.com/api/en-us/catalog/track/v1/docs.html#operation/Track%20by%20Tracking%20Number)  
Retrieve shipment status based on tracking numbers.

**Response**

```
{
  "transactionId": "624deea6-b709-470c-8c39-4b5511281492",
  "customerTransactionId": "AnyCo_order123456789",
  "output": {
    "completeTrackResults": [
      {
        "trackingNumber": "123456789012",
        "trackResults": [
          {}
        ]
      }
    ],
    "alerts": "TRACKING.DATA.NOTFOUND -  Tracking data unavailable"
  }
}
```

## Jamf Pro

**GET**  
[/JSSResource/computers](https://developer.jamf.com/jamf-pro/reference/findcomputers)  
Retrieve computer data for asset identification.

**Response**

```
[
  {
    "size": 1,
    "computer": {
      "id": 1,
      "name": "string"
    }
  }
]
```

**DELETE**  
[/JSSResource/computers/id/{id}](https://developer.jamf.com/jamf-pro/reference/deletecomputerbyid)  
Delete a computer record from Jamf Pro after recovery.

**Response**

```
{
  "computer": {
    "id": "1"
  }
}
```


## Slack

**POST**  
[/chat.postMessage](https://api.slack.com/methods/chat.postMessage)  
Send a message to a Slack channel or direct message.

**Response**

```
{
    "ok": true,
    "channel": "C123ABC456",
    "ts": "1503435956.000247",
    "message": {
        "text": "Here's a message for you",
        "username": "ecto1",
        "bot_id": "B123ABC456",
        "attachments": [
            {
                "text": "This is an attachment",
                "id": 1,
                "fallback": "This is an attachment's fallback"
            }
        ],
        "type": "message",
        "subtype": "bot_message",
        "ts": "1503435956.000247"
    }
}
```

**POST**  
[/chat.update](https://api.slack.com/methods/chat.update)  
Update an existing message with new content.

**Response**

```
{
    "ok": true,
    "channel": "C123ABC456",
    "ts": "1401383885.000061",
    "text": "Updated text you carefully authored",
    "message": {
        "text": "Updated text you carefully authored",
        "user": "U34567890"
    }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
