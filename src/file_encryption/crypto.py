import os
from cryptography.fernet import Fernet, InvalidToken

def encrypt_file(filepath: str, key: bytes) -> str:
    """Encrypts a file securely."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    fernet = Fernet(key)
    with open(filepath, 'rb') as f:
        data = f.read()
        
    encrypted = fernet.encrypt(data)
    
    out_path = filepath + ".enc"
    with open(out_path, 'wb') as f:
        f.write(encrypted)
        
    return out_path
    
def decrypt_file(filepath: str, key: bytes, out_path: str = None) -> str:
    """Decrypts a file securely."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    fernet = Fernet(key)
    with open(filepath, 'rb') as f:
        encrypted_data = f.read()
        
    try:
        data = fernet.decrypt(encrypted_data)
    except InvalidToken:
        raise ValueError("Invalid decryption key or corrupted file.")
    
    if not out_path:
        if filepath.endswith(".enc"):
            out_path = filepath[:-4]
        else:
            out_path = filepath + ".dec"
            
    with open(out_path, 'wb') as f:
        f.write(data)
        
    return out_path
