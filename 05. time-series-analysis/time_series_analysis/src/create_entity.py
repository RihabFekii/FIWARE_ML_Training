import requests
import datetime
import logging

logger = logging.getLogger(__name__)

def create_or_update_entity(weather_data, CITY, CB_URL, CB_HEADERS):
    entity_id = f"Weather-{CITY}"
    check_url = f"{CB_URL}/{entity_id}"
    
    payload = {
        "timestamp": {
            "value": datetime.datetime.now().isoformat(),
            "type": "DateTime"
        },
        "temperature": {
            "value": weather_data['main']['temp'],
            "type": "Float"
        },
        "pressure": {
            "value": weather_data['main']['pressure'],
            "type": "Integer"
        },
        "humidity": {
            "value": weather_data['main']['humidity'],
            "type": "Integer"
        },
        "wind_speed": {
            "value": weather_data['wind']['speed'],
            "type": "Float"
        },
        "clouds": {
            "value": weather_data['clouds']['all'],
            "type": "Integer"
        }
    }

    try:
        # Check if entity exists
        check_response = requests.get(check_url, headers=CB_HEADERS)
        
        if check_response.status_code == 200:
            # Entity exists, update it
            update_url = f"{CB_URL}/{entity_id}/attrs"
            response = requests.patch(update_url, headers=CB_HEADERS, json=payload)
            if response.status_code == 204:
                logger.info(f"Entity {entity_id} updated successfully")
            else:
                logger.error(f"Failed to update entity. Status code: {response.status_code}, Response: {response.text}")
        elif check_response.status_code == 404:
            # Entity doesn't exist, create it
            create_payload = {
                "id": entity_id,
                "type": "WeatherObserved",
                **payload
            }
            response = requests.post(CB_URL, headers=CB_HEADERS, json=create_payload)
            if response.status_code == 201:
                logger.info(f"Entity {entity_id} created successfully")
            else:
                logger.error(f"Failed to create entity. Status code: {response.status_code}, Response: {response.text}")
        else:
            logger.error(f"Unexpected response when checking entity. Status code: {check_response.status_code}")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error occurred while interacting with Context Broker: {e}")

