import logging
import configparser

from src.io.dbHandler import create_db, insert_offers
from src.io.scraper import scrape_jobs

# Set up logger
# TODO This config here is the same as in __init__. See if there is an easy way to avoid duplication (without hacks).
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# define handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def get_jobs():

    # Get my config
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    url = config.get('TECNO', 'TECNO_24H_URL')
    keywords_list = config.get('SCRAPPER', 'KEYWORDS').split(',')

    # Create DB if it doesn´t exist
    create_db()

    for k in keywords_list:
        logger.info("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
        logger.info(f"Looking for keyword: {k}")
        logger.info("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
        logger.info("Looking for jobs...")
        all_jobs = scrape_jobs(url, k)

        logger.info("Comparing with DB...")
        successfully_inserted = insert_offers(all_jobs)

        logger.info("*******RESULTS*******")
        logger.info("I have found {} new positions and {} old ones.".format(len(successfully_inserted), len(all_jobs) - len(successfully_inserted)))
        for j in successfully_inserted:
            logger.info(j)


if __name__ == "__main__":

    get_jobs()
