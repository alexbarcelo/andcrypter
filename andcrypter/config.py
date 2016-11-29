import configparser
from logging import getLogger

logger = getLogger(__name__)


class Config:
	"""Configuration object."""
	def __init__(self, ini_path):
		"""Load the configuration from the .ini file."""
		logger.info("Loading configuration file: %s", ini_path)
		self._config = configparser.ConfigParser()
		self._config.read(ini_path)
