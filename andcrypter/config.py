import configparser
from logging import getLogger

import binascii

logger = getLogger(__name__)


class Config:
	"""Configuration object."""
	def __init__(self, ini_path):
		"""Load the configuration from the .ini file."""

		# Store the path for the store operations
		self._ini_path = ini_path

		logger.info("Loading configuration file: %s", ini_path)
		self._config = configparser.ConfigParser()
		self._config.read(ini_path)

	def has_volume(self, volume_name):
		"""The volumes are actually stored as sections in the .ini file."""
		if volume_name == "common":
			raise NameError("A volume cannot be named 'common'")
		return self._config.has_section(volume_name)

	def store_volume(self, volume_name, part_uuid, salt, encrypted_key):
		"""Store the settings for a (new) volume."""
		if volume_name == "common":
			raise NameError("A volume cannot be named 'common'")

		# Force override
		self._config.remove_section(volume_name)
		self._config[volume_name] = {
			"PartUUID": part_uuid,
			"Salt": binascii.hexlify(salt).decode(),
			"EncryptedKey": binascii.hexlify(encrypted_key).decode(),
		}

		self._store()

	def _store(self):
		with open(self._ini_path, 'w') as configfile:
			self._config.write(configfile)
