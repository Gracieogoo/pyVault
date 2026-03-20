# pyVault

A comprehensive python security tool kit featuring password management, file encryption, network scanning and security analysis.

## 🛠️ Tools & Libraries Used

### Third-Party Libraries
*   **`cryptography`**: The core security engine. Handles symmetric encryption (`Fernet`) for locking your vault and files, and Key Derivation (`PBKDF2HMAC`) for turning your Master Password into an unbreakable cryptographic key.
*   **`click`**: Powers the Command Line Interface (CLI). Makes passing arguments, flags, and building sub-menus (like `vault`, `crypto`, `network`) seamless.
*   **`rich`**: The aesthetic engine. Applies styling, colors, and structured tables to make the terminal output visually appealing and easy to read.
*   **`requests`**: Handles web traffic to grab live IP geolocation information from external APIs.
*   **`pytest`**: The framework used to write and execute automated unit tests to ensure the security logic works properly.

### Python Built-in Modules
*   **`socket` & `concurrent.futures`**: Used together to build an extremely fast, multi-threaded port scanner.
*   **`hashlib`**: Used to compute cryptographic hashes of files (SHA-256).
*   **`secrets` & `string`**: Used instead of the basic `random` module to generate cryptographically safe random passwords.
*   **`msvcrt` & `sys`**: Windows-specific modules used to capture keystrokes directly so we can draw asterisks (`*`) in the terminal.

---

## 🚀 Comprehensive Feature List

Below is everything you can do, organized by the command groups available in the CLI.

### 1. Password Manager (`vault`)
A secure, encrypted local database for your credentials.
*   **Add/Generate Passwords**: `python -m src.main vault add <service> <username>`
    *   Automatically generates a 16-character cryptographically strong password (guaranteeing uppercase, lowercase, numbers, and symbols) and saves it to your encrypted vault. You can also provide your own password using the `-p` flag.
*   **Retrieve Passwords**: `python -m src.main vault get <service>`
    *   Prompts for your master password, zeroes in on the service, and neatly prints the username and decrypted password in a `rich` table.
*   **List Services**: `python -m src.main vault list`
    *   Lists all the service names currently stored in your vault without exposing the credentials.

### 2. File Encryption (`crypto`)
Encrypt and decrypt external files (documents, images, text files) using a password.
*   **Encrypt a File**: `python -m src.main crypto encrypt <path_to_file>`
    *   Reads the file, prompts for a password, heavily encrypts the file's binary data, and outputs a new file ending in `.enc` (leaving the original untouched).
*   **Decrypt a File**: `python -m src.main crypto decrypt <path_to_file.enc>`
    *   Takes an encrypted file and the correct password, and restores the file back to its original fully readable state.

### 3. Network Scanning (`network`)
Analyze targets on a network or the wider internet.
*   **Port Scanner**: `python -m src.main network scan <ip_or_domain> --start 1 --end 1024`
    *   Rapidly spans hundreds of threads to map out open TCP ports on a given target machine to see what services (like HTTP, SSH, FTP) are running.
*   **IP Geolocation**: `python -m src.main network ipinfo <ip_address>`
    *   Reaches out of your network to pull down geographical data (City, Country, Region, ISP, coordinates) for any given public IP address.

### 4. Security Analysis (`check`)
Locally analyze strings and files to assess their security posture.
*   **Password Analyzer**: `python -m src.main check password "MyPass!"`
    *   Evaluates a plaintext password based on entropy rules. It checks the length, character variations, and structural patterns, then returns a score (Weak, Moderate, Strong) alongside specific feedback on how to improve it.
*   **File Hashing**: `python -m src.main check hash <path_to_file>`
    *   Computes the SHA-256 checksum of a file. This is useful for file integrity verification or for comparing the output hash against malware checksum databases.

---

## ⚙️ Setup & Installation (For New Users)
If you are downloading or cloning this project for the first time, follow these exact steps to set it up securely on your machine:

1. **Install Python**: Make sure you have Python 3.14 (or compatible version) installed on your system.
2. **Open your Terminal**: Open PowerShell (Windows) or Terminal (Mac/Linux) and navigate inside the `pyVault` directory.
3. **Create the Virtual Environment**: Run the following command to isolate the toolkit's dependencies:
   ```powershell
   python -m venv venv
   ```
4. **Activate the Environment**: 
   * On Windows: `.\venv\Scripts\Activate.ps1`
   * On Mac/Linux: `source venv/bin/activate`
5. **Install the Requirements**:
   ```powershell
   pip install -r requirements.txt
   ```
6. **Start Using It**: The toolkit is completely set up! Run this to see the main menu:
   ```powershell
   python -m src.main --help
   ```
*(Note: Your private vault database and keys are uniquely generated on your local machine and blocked from being uploaded via `.gitignore`.)*
