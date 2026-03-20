import os

# Base directory setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Vault files configuration
VAULT_DB_PATH = os.path.join(DATA_DIR, 'vault.db')
SALT_PATH = os.path.join(DATA_DIR, 'salt.key')

# Security tool configuration parameters
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
