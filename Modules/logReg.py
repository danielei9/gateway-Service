import logging
from datetime import datetime
#------------------------- Start Logging ---------------------------------
logging.basicConfig(filename='Display.log', level=logging.DEBUG)
logging.debug(datetime.now())
logging.debug('Starting...')
#--------------------------------------------------------------------------

def logRegister(txt):
    logging.debug(datetime.now())
    logging.debug(txt)

def logWarning(txt):
    logging.warning(datetime.now())
    logging.warning(txt)