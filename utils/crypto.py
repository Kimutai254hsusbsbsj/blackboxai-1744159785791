from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
from typing import Optional

class EncryptionManager:
    def __init__(self, key: str):
        """Initialize with encryption key (will be padded to valid length)"""
        # Pad key if needed to reach valid length
        key_len = len(key)
        if key_len < 16:
            self.key = key.ljust(16, '\0').encode('utf-8')
        elif 16 < key_len < 24:
            self.key = key.ljust(24, '\0').encode('utf-8')
        elif 24 < key_len < 32:
            self.key = key.ljust(32, '\0').encode('utf-8')
        elif key_len > 32:
            self.key = key[:32].encode('utf-8')
        else:
            self.key = key.encode('utf-8')

    def encrypt_data(self, data: str) -> Optional[str]:
        """Encrypt data using AES-256-CBC"""
        try:
            iv = os.urandom(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
            return base64.b64encode(iv + ct_bytes).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    def decrypt_data(self, enc_data: str) -> Optional[str]:
        """Decrypt data using AES-256-CBC"""
        try:
            enc_data = base64.b64decode(enc_data)
            iv = enc_data[:16]
            ct = enc_data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None

def decrypt_data(file_path: str, key: str) -> Optional[str]:
    """Convenience function to decrypt a file's contents"""
    try:
        with open(file_path, 'r') as f:
            enc_data = f.read()
        manager = EncryptionManager(key)
        return manager.decrypt_data(enc_data)
    except Exception as e:
        print(f"File decryption error: {e}")
        return None
