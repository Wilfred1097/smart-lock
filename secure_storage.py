import os
from kivy.storage.jsonstore import JsonStore
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64

# A unique salt generated for your application.
# It's important that this value remains constant once set.
SALT = b'salt_for_Wilfred1097_20250701'

KEY_PASSWORD = b'Mv!App-s3cr3t-K3y-p@ssw0rd-2025-W1lfr3d'


class SecureStorage:
    def __init__(self, filename="data.json"):
        # The path where the app will store its data
        data_dir = os.path.dirname(os.path.abspath(__file__))
        self.store = JsonStore(os.path.join(data_dir, filename))
        self._generate_key()

    def _generate_key(self):
        """Generates a secure encryption key from a password and salt."""
        # Explicitly provide the backend for Android compatibility
        backend = default_backend()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SALT,
            iterations=480000,
            backend=backend,  # This line is the fix
        )
        key = base64.urlsafe_b64encode(kdf.derive(KEY_PASSWORD))
        self.fernet = Fernet(key)

    def encrypt(self, data):
        """Encrypts data."""
        if not data:
            return ""
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """Decrypts data."""
        if not encrypted_data:
            return ""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            # Handle cases where decryption fails
            return ""

    def get_value(self, key, default=None, is_encrypted=False):
        """
        Gets a value from the store, decrypting it if necessary.
        Returns the default value if the key does not exist.
        """
        if self.store.exists(key):
            value = self.store.get(key)
            if is_encrypted:
                return self.decrypt(value.get('data'))
            else:
                return value.get('data')
        return default

    def set_value(self, key, value, is_encrypted=False):
        """Sets a value in the store, encrypting it if necessary."""
        data_to_store = self.encrypt(value) if is_encrypted else value
        self.store.put(key, data=data_to_store)
