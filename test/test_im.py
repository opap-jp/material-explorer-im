import unittest
from src import im

class ImageMagickTestCase(unittest.TestCase):
    def setUp(self):
        self.app = im.app.test_client()

    def tearDown(self):
        None

    def test_1_is_1(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
