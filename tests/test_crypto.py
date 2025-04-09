import os
import tempfile
import unittest
from utils.crypto import EncryptionManager, decrypt_data

class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.key = "ThisIsATestKey1234567890123456"  # 32 bytes
        self.test_data = "This is a secret message"
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'encrypted.txt')

    def test_encrypt_decrypt(self):
        manager = EncryptionManager(self.key)
        encrypted = manager.encrypt_data(self.test_data)
        self.assertIsNotNone(encrypted)
        
        decrypted = manager.decrypt_data(encrypted)
        self.assertEqual(decrypted, self.test_data)

    def test_file_decryption(self):
        manager = EncryptionManager(self.key)
        encrypted = manager.encrypt_data(self.test_data)
        with open(self.test_file, 'w') as f:
            f.write(encrypted)
        
        decrypted = decrypt_data(self.test_file, self.key)
        self.assertEqual(decrypted, self.test_data)

    def test_invalid_key(self):
        # Should now accept any key length due to padding
        try:
            EncryptionManager("shortkey")
            EncryptionManager("")
        except Exception as e:
            self.fail(f"EncryptionManager failed with valid input: {e}")

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
