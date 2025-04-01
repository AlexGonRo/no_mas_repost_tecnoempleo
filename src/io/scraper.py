import logging
import time
import re
from datetime import datetime

from src.popos.offer import Offer
from src.utils.utils import get_soup

"""
Modificado a partir de la versión del proyecto de mankolepanto:
https://github.com/mankolepanto/Scrap_TecnoEmpleo
"""
logger = logging.getLogger(__name__)

def extract_info(job):
    """Extrae la información relevante de una oferta de trabajo."""
    try:
        offer = Offer()

        ''' Extraer la fecha de publicación '''
        date_div = job.find('div', class_='col-12 col-lg-3 text-gray-700 pt-2 text-right hidden-md-down')
        date_str = date_div.contents[0].strip() if date_div and date_div.contents else "Fecha no encontrada"
        offer.date = datetime.strptime(date_str, "%d/%m/%Y")

        ''' Extraer el nombre del trabajo '''
        job_element = job.find('a', class_='font-weight-bold text-cyan-700')
        offer.job_name = job_element.get_text().strip() if job_element else "Trabajo no encontrado"

        ''' Extraer descripción '''
        job_element = job.find('span', class_='hidden-md-down text-gray-800')
        offer.description = job_element.get_text().strip() if job_element else "Descripción no encontrada"

        '''Extraer el enlace'''
        link_tag = job.select_one('h3.fs-5.mb-2 a')
        offer.link = link_tag['href'] if link_tag else "Enlace no encontrado"

        # Extraer id de la oferta
        if offer.link != "Enlace no encontrado":
            match = re.search(r'/rf-([a-zA-Z0-9]+)', offer.link)
            offer.id = match.group(1) if match else "ID no encontrado"

        # Extraer nombre de la empresa
        a_tag = job.find('a', class_='text-primary link-muted')
        offer.company_name = a_tag.get_text().strip() if a_tag else "Empresa no encontrada"

        return offer

    except Exception as e:
        logger.error(f"Error al procesar la oferta de trabajo: {e}")
        return None

def find_next_page(soup):
    """Busca y devuelve el enlace de la siguiente página, si existe."""
    next_page_tag = soup.find('a', class_='page-link', string='siguiente')
    return next_page_tag['href'] if next_page_tag else None


def scrape_jobs(url, keyword):
    """Realiza el scraping de ofertas de trabajo desde la URL proporcionada y crea un CSV con los datos del día objetivo."""
    all_jobs = []
    full_url = url + "?te=" + keyword

    while full_url:
        logger.info(f"Scrapping {full_url}")
        soup = get_soup(full_url)
        ofertas = soup.find_all('div', class_='p-3 border rounded mb-3 bg-white')
        # Si no hemos encontrado trabajos en esta página
        if not ofertas:
            logger.info("No jobs today.")
            return all_jobs

        for job in ofertas:
            job_info = extract_info(job)

            if job_info:
                all_jobs.append(job_info)

        # Buscar la siguiente página si es que la hay
        full_url = find_next_page(soup)
        if full_url:
            logger.info(f"Next page...")
            time.sleep(3)
        else:
            logger.info("No more pages left.")


    return all_jobs