import logging
import re

logging.basicConfig(
    filename='exivium.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log(mensagem: str):
    if re.search(r'\berro\b', mensagem, re.IGNORECASE):
        logging.error(mensagem)
    else:
        logging.info(mensagem)
    print(mensagem)