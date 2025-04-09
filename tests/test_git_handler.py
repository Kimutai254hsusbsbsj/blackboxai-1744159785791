import os
import tempfile
import unittest
from unittest.mock import patch
from utils.git_handler import clone_repository

class TestGitHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    @patch('utils.git_handler.Repo.clone_from')
    def test_clone_repository_success(self, mock_clone):
        test_url = "https://github.com/example/test.git"
        result = clone_repository(test_url, self.temp_dir)
        self.assertEqual(result, os.path.join(self.temp_dir, "test"))
        mock_clone.assert_called_once()

    @patch('utils.git_handler.Repo.clone_from')
    def test_clone_repository_failure(self, mock_clone):
        mock_clone.side_effect = Exception("Clone failed")
        test_url = "https://github.com/example/test.git"
        result = clone_repository(test_url, self.temp_dir)
        self.assertIsNone(result)

    @patch('utils.git_handler.Repo.clone_from')
    def test_clone_to_existing_dir(self, mock_clone):
        test_url = "https://github.com/example/test.git"
        # Create dummy file in temp dir
        with open(os.path.join(self.temp_dir, 'dummy'), 'w') as f:
            f.write('test')
        result = clone_repository(test_url, self.temp_dir)
        self.assertIsNone(result)
        mock_clone.assert_not_called()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
