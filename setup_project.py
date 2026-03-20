import os

# Define project structure
structure = {
    'src': {
        '__init__.py': '',
        'main.py': '',
        'config.py': '',
        'password_manager': {
            '__init__.py': '',
        },
        'file_encryption': {
            '__init__.py': '',
        },
        'network_tools': {
            '__init__.py': '',
        },
        'utils': {
            '__init__.py': '',
        },
        'web_dashboard': {
            '__init__.py': '',
            'templates': {}
        }
    },
    'tests': {
        '__init__.py': '',
        'test_password_manager.py': '',
    },
    'docs': {
        'USAGE.md': '',
        'API.md': '',
    },
    'data': {
        '.gitkeep': '',
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            print(f"✓ Created directory: {path}")
            create_structure(path, content)
        else:
            # It's a file
            with open(path, 'w') as f:
                f.write(content)
            print(f"✓ Created file: {path}")

# Create requirements.txt at root
with open('requirements.txt', 'w') as f:
    f.write('''# Core dependencies
cryptography==41.0.7
flask==3.0.0
python-dotenv==1.0.0

# Security tools
bcrypt==4.1.2

# Network tools
scapy==2.5.0
requests==2.31.0

# Data handling
pandas==2.1.4

# CLI interface
rich==13.7.0
click==8.1.7

# Testing
pytest==7.4.3
pytest-cov==4.1.0
''')

print("\n🚀 Setting up PyVault project structure...\n")
create_structure('.', structure)
print("\n✅ Project structure created successfully!")
print("\nNext steps:")
print("1. python -m venv venv")
print("2. venv\\Scripts\\activate")
print("3. pip install -r requirements.txt")