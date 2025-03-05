import logging
from fetch_data import get_weather_data, send_to_context_broker
from create_entity import create_or_update_entity
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load config from config.json
with open('./config/config.json', 'r') as config_file:
    config = json.load(config_file)

CITY = config['city']
CB_URL = config['context_broker_url']
CB_HEADERS = config['context_broker_headers']

def main():
    weather_data = get_weather_data()
    if weather_data:
        create_or_update_entity(weather_data, CITY, CB_URL, CB_HEADERS)
        send_to_context_broker(weather_data)
    else:
        logger.error("Failed to retrieve weather data")

if __name__ == "__main__":
    main()
