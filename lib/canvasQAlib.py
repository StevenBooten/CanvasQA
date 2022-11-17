import logging
from simple_settings import settings

def initialiseLogging(logFileName=None):
    """Set up basic logging information for all CAR generation
    Use default MIGRATION_LOGFILE unless filename specified
    Specified log file is just a name used with MIGRATION_BASE
    """

    if logFileName is None:
        logFileName = settings.MIGRATION_LOGFILE
    else:
        logFileName = f"{settings.MIGRATION_BASE}{logFileName}"

    logging.basicConfig( level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(filename)s %(funcName)s %(lineno)d: %(message)s',
        filename=logFileName )