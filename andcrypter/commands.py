from logging import getLogger

logger = getLogger(__name__)


def create(config, parse_args):
	logger.info("Calling 'create' subcommand")


def mount(config, parse_args):
	logger.info("Calling 'mount' subcommand")


def umount(config, parse_args):
	logger.info("Calling 'umount' subcommand")


def android(config, parse_args):
	logger.info("Calling 'android' subcommand")
