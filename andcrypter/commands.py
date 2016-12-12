import uuid
from getpass import getpass
from subprocess import check_output, CalledProcessError
from logging import getLogger

import binascii

from andcrypter import mincrypt

logger = getLogger(__name__)


def create(config, parse_args):
    logger.info("Calling 'create' subcommand")

    # Confirm what is about to happen
    c = input("Contents on %s will be removed.\n"
              "Are you sure that this is a valid partition?\n"
              "Type 'yes' to continue: " % parse_args.dev_path)
    if c != "yes":
        print("Aborted")
        return

    if config.has_volume(parse_args.volume_name):
        # Confirm what is about to happen
        c = input("You already have a partition named %s set up. "
                  "Are you sure you want to override it?\n"
                  "Type 'yes' to continue: " % parse_args.dev_path)
        if c != "yes":
            print("Aborted")
            return

    print("\nProceeding to format partition %s as the '%s' encrypted partition"
          % (parse_args.dev_path, parse_args.volume_name))

    # Maybe this can be achieved in Python, still looking
    try:
        ret = check_output(["sudo", "blockdev", "--getsize", parse_args.dev_path])
    except CalledProcessError:
        print("Call to `blockdev --getsize` failed. Maybe `sudo` error or invalid partition?")
        return

    logger.debug("blockdev call returned: %s", ret)
    blocksize = int(ret.strip().decode())
    logger.info("Using %d as the size of the partition", blocksize)

    # Maybe also this can be achieved in Python...
    try:
        ret = check_output(["sudo", "blkid", "-o", "value", parse_args.dev_path])
    except CalledProcessError:
        print("Call to `blkid` failed. Maybe `sudo` error or invalid partition?")
        return
    logger.debug("blkid call returned: %s", ret)
    partuuid = uuid.UUID(hex=ret.strip().decode())

    logger.info("Using {%s} as the partition UUID", partuuid)

    print()

    password = getpass("Type a password to protect your encrypted partition: ")
    if len(password) < 6:
        print("\nRefusing to use a password shorter than 6 characters")
        return

    check_password = getpass("Type the password again: ")
    if password != check_password:
        print("\nThe passwords do not match, aborting")
        return

    key = mincrypt.create_key()
    salt, key_encrypted = mincrypt.encrypt_key(key, bytes(password, "utf-8"))
    logger.debug("Using the following salt: %s", binascii.hexlify(salt))
    logger.debug("The encrypted key is the following: %s", binascii.hexlify(key_encrypted))

    config.store_volume(parse_args.volume_name,
                        part_uuid=partuuid,
                        salt=salt,
                        encrypted_key=key_encrypted)


def mount(config, parse_args):
    logger.info("Calling 'mount' subcommand")


def umount(config, parse_args):
    logger.info("Calling 'umount' subcommand")


def android(config, parse_args):
    logger.info("Calling 'android' subcommand")
