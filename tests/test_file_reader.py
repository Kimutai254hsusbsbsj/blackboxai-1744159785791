import os
import tempfile
import unittest
from utils.file_reader import read_code_file

class TestFileReader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.py')
        with open(self.test_file, 'w') as f:
            f.write('print("Hello World")')

    def test_read_valid_file(self):
        content = read_code_file(self.test_file)
        self.assertEqual(content.strip(), 'print("Hello World")')

    def test_read_nonexistent_file(self):
        content = read_code_file('nonexistent.txt')
        self.assertIsNone(content)

    def tearDown(self):
        os.remove(self.test_file)
        os.rmdir(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
