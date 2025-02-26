import requests
import json
import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CITY = config['city']
CB_URL = config['context_broker_url']
CB_HEADERS = config['context_broker_headers']

def create_entity(weather_data):
    entity_id = f"Weather-{CITY}"
    payload = {
        "id": entity_id,
        "type": "WeatherObserved",
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
    response = requests.post(CB_URL, headers=CB_HEADERS, json=payload)
    if response.status_code == 201:
        logger.info(f"Entity {entity_id} created successfully")
    else:
        logger.error(f"Failed to create entity. Status code: {response.status_code}, Response: {response.text}")
