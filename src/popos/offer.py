class Offer:

    def __init__(self, date=None, job_name=None, description=None, link=None, id=None, company_name=None):
        self.date = date
        self.job_name = job_name
        self.description = description
        self.link = link
        self.id = id
        self.company_name = company_name

    def __repr__(self):
        # Returns a string representation of the Offer object
        return f"Offer(offer_id={self.id}, job_name={self.job_name}, company_name={self.company_name}, date={self.date}, link={self.link})"