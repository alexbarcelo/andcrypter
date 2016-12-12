"""Minimal Cryptography stuff required by Andcrypter."""
import hashlib
import os


def create_key():
    """Quite minimal: 16 bytes of randomness."""
    return os.urandom(16)


def encrypt_key(key, password):
    """Encrypt the given key through the provided password.

    :param bytes key: The 16 bytes key for the volume.
    :param bytes password: The password (in bytes form) provided by the user.
    """
    salt = os.urandom(16)
    key_opener = hashlib.pbkdf2_hmac('sha256', password, salt, 100000, dklen=16)
    key_encrypted = bytes(a ^ b for a, b in zip(key, key_opener))

    return salt, key_encrypted
