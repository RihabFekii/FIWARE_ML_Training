import requests
import json
import datetime
import logging
import os
from dotenv import load_dotenv
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CITY = config['city']
CB_URL = config['context_broker_url']
CB_HEADERS = config['context_broker_headers']

OWM_API_KEY = os.getenv("OWM_API_KEY")
OWM_URL = os.getenv("OWM_URL")

def get_weather_data():
    params = {
        "q": CITY,
        "appid": OWM_API_KEY,
        "units": "metric"
    }
    response = requests.get(OWM_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        logger.info(f"Successfully retrieved weather data for {CITY}")
        logger.info(f"API Response: {json.dumps(data, indent=2)}")
        return data
    logger.error(f"Failed to retrieve weather data for {CITY}. Status code: {response.status_code}, Response: {response.text}")
    return None


def send_to_context_broker(weather_data):
    timestamp = datetime.datetime.now().isoformat()
    entity_id = f"Weather-{CITY}"
    payload = {
        "timestamp": {
            "value": timestamp,
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
    logger.info(f"Sending payload to Context Broker: {json.dumps(payload, indent=2)}")
    logger.info(f"Context Broker URL: {CB_URL}/{entity_id}/attrs")
    logger.info(f"Context Broker Headers: {json.dumps(CB_HEADERS, indent=2)}")
    
    response = requests.patch(f"{CB_URL}/{entity_id}/attrs", headers=CB_HEADERS, data=json.dumps(payload))
    logger.info(f"Context Broker Response Status Code: {response.status_code}")
    logger.info(f"Context Broker Response Text: {response.text}")
    
    if response.status_code == 204:
        logger.info("Data sent successfully to Context Broker")
    else:
        logger.error(f"Failed to send data to Context Broker. Status code: {response.status_code}, Response: {response.text}")
