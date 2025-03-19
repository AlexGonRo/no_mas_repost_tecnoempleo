from datetime import datetime, timedelta
import configparser
import os
from scraper import scrape_jobs
from dbHandler import create_db, insert_offers


def get_last_24h():

    # Get my config
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    url = config.get('TECNO', 'TECNO_24H_URL')
    keywords_list = config.get('SCRAPPER', 'KEYWORDS').split(',')

    # Create DB if it doesn´t exist
    create_db()

    for k in keywords_list:
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
        print(f"Buscando trabajos para la búsqueda: {k}")
        print("=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+")
        print("Looking for jobs...")
        all_jobs = scrape_jobs(url, k)

        print("Comparing with DB...")
        successfully_inserted = insert_offers(all_jobs)

        print("*******RESULTS*******")
        print("He encontrado {} ofertas nuevas y {} ofertas repetidas.".format(len(successfully_inserted), len(all_jobs) - len(successfully_inserted)))
        for j in successfully_inserted:
            print(j)


if __name__ == "__main__":

    get_last_24h()
