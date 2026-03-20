import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def generate_salt(salt_path: str):
    """"Generate and save a salt for PBKDF2."""
    salt = os.urandom(16)
    with open(salt_path, 'wb') as f:
        f.write(salt)
    return salt

def get_or_create_salt(salt_path: str) -> bytes:
    if os.path.exists(salt_path):
        with open(salt_path, 'rb') as f:
            return f.read()
    else:
        return generate_salt(salt_path)

def derive_key(master_password: str, salt: bytes) -> bytes:
    """Derive a 32-byte key from the given master password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)
