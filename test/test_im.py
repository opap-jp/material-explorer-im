import unittest
from src import im

class ImageMagickTestCase(unittest.TestCase):
    def setUp(self):
        self.app = im.app.test_client()

    def tearDown(self):
        None

    def test_ping(self):
        response = self.app.get("/ping")
        self.assertEqual(response.data, b"pong")

if __name__ == "__main__":
    unittest.main()
