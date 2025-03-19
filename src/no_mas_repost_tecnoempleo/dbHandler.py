import sqlite3

# Función para crear la base de datos y la tabla
def create_db():
    conn = sqlite3.connect('offers.db') # TODO Hardcodeado aquí de mala manera, pero bueno
    cursor = conn.cursor()

    #cursor.execute('''
    #DROP TABLE IF EXISTS offers
    #''')

    # Crear la tabla 'offers' si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS offers (
        id TEXT PRIMARY KEY,
        job_name TEXT NOT NULL,
        company_name TEXT NOT NULL,
        date TEXT NOT NULL,
        link TEXT NOT NULL,
        description TEXT,
        UNIQUE(job_name, company_name, description)  -- Asegura que no haya ofertas duplicadas
    )
    ''')

    conn.commit()
    conn.close()

# Función para insertar una oferta en la base de datos
def insert_offer(offer):
    conn = sqlite3.connect('offers.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
        INSERT INTO offers (id, job_name, company_name, date, link, description)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (offer.id, offer.job_name, offer.company_name, offer.date.isoformat(), offer.link, offer.description))
        conn.commit()
        print(f"Offer '{offer.job_name}' at '{offer.company_name}' added successfully.")
        return offer  # Indicate successful insertion
    except sqlite3.IntegrityError as a:
        # Si hay un error de integridad (como una oferta duplicada), no hacemos nada
        print(f"Offer '{offer.job_name}' at '{offer.company_name}' is a duplicate and was not added.")
        return False  # Indicate duplicate
    finally:
        conn.close()


# Función para insertar múltiples ofertas
def insert_offers(offers):
    inserted_offers = []
    for offer in offers:
        offer = insert_offer(offer)
        if offer:
            inserted_offers.append(offer)

    return inserted_offers