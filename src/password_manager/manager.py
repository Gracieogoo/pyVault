import os
import json
import secrets
import string
from cryptography.fernet import Fernet, InvalidToken
from src.config import VAULT_DB_PATH

def generate_password(length: int = 16, use_special: bool = True) -> str:
    """Generate a strong random password."""
    alphabet = string.ascii_letters + string.digits
    special = "!@#$%^&*()-_+="
    
    if not use_special:
        return "".join(secrets.choice(alphabet) for _ in range(length))
        
    pwd = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(special)
    ]
    all_chars = alphabet + special
    pwd += [secrets.choice(all_chars) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(pwd)
    return "".join(pwd)

class VaultManager:
    """Manages secure password storage."""
    def __init__(self, key: bytes):
        self.fernet = Fernet(key)
        self.vault_path = VAULT_DB_PATH

    def _load_vault(self) -> dict:
        if not os.path.exists(self.vault_path):
            return {}
        with open(self.vault_path, 'rb') as f:
            encrypted_data = f.read()
            
        if not encrypted_data:
             return {}
             
        try:
            data = self.fernet.decrypt(encrypted_data)
            return json.loads(data.decode('utf-8'))
        except InvalidToken:
            raise ValueError("Invalid master password or corrupted vault data.")

    def _save_vault(self, data: dict):
        json_data = json.dumps(data).encode('utf-8')
        encrypted_data = self.fernet.encrypt(json_data)
        with open(self.vault_path, 'wb') as f:
            f.write(encrypted_data)

    def add_password(self, service: str, username: str, password: str):
        vault = self._load_vault()
        vault[service] = {"username": username, "password": password}
        self._save_vault(vault)

    def get_password(self, service: str) -> dict:
        vault = self._load_vault()
        return vault.get(service)
        
    def list_services(self) -> list:
        return list(self._load_vault().keys())
