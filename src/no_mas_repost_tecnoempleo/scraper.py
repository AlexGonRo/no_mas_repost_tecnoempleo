import re
from datetime import datetime

from src.no_mas_repost_tecnoempleo.classes.offer import Offer
from src.no_mas_repost_tecnoempleo.utils import get_soup

"""
Modificado a partir de la versión del proyecto de mankolepanto:
https://github.com/mankolepanto/Scrap_TecnoEmpleo/tree/main
"""

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
        print(f"Error al procesar la oferta de trabajo: {e}")
        return None


def scrape_jobs(url, keyword):
    """Realiza el scraping de ofertas de trabajo desde la URL proporcionada y crea un CSV con los datos del día objetivo."""
    all_jobs = []
    full_url = url + "&te=" + keyword  # TODO Menuda chapuza ese &, también te digo

    soup = get_soup(full_url)
    ofertas = soup.find_all('div', class_='p-3 border rounded mb-3 bg-white')
    # Si no hemos encontrado trabajos en esta página
    if not ofertas:
        print("NO HAY TRABAJOS HOY.")
        return all_jobs

    for job in ofertas:
        job_info = extract_info(job)

        if job_info:
            all_jobs.append(job_info)

    # Buscar la siguiente página si es que la hay
    # TODO Tendría que arreglar esto...
    '''url = find_next_page(soup)
    if url:
        print(f"Pasando a la siguiente página: {url}")
        time.sleep(3)
    else:
        print("No hay más páginas.")
    '''

    return all_jobs