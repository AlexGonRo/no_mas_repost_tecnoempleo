# instantiate logger
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# define handler and formatter
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)