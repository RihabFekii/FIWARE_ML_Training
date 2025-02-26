import logging

from fetch_data import get_weather_data, send_to_context_broker
from create_entity import create_entity


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    create_entity(get_weather_data())  # Create entity on first run
    weather_data = get_weather_data()
    if weather_data:
        send_to_context_broker(weather_data)
    else:
        logger.error("Failed to retrieve weather data")

if __name__ == "__main__":
    main()