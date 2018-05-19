import unittest
from os import path
from src import im
from io import BytesIO

THUMB_LENGTH = str(290)

def resolve_image(name):
    p = path.dirname(__file__) + "/fixture/images/" + name
    with open(p, "rb") as f:
        return (BytesIO(f.read()), name)

class ImageMagickTestCase(unittest.TestCase):
    def setUp(self):
        self.app = im.app.test_client()

    def tearDown(self):
        None

    def test_ping(self):
        response = self.app.get("/ping")
        self.assertEqual(response.data, b"pong")

    def test_resize_with_valid_params(self):
        response = self.app.post("/resize",
            content_type='multipart/form-data',
            data=dict(
                width=THUMB_LENGTH,
                height=THUMB_LENGTH,
                data=resolve_image("kosys.png"),
            )
        )
        self.assertEqual(response.status_code, 200)

    def upload(self, params):
        return self.app.post("/resize",
            content_type='multipart/form-data',
            data=params
        )
if __name__ == "__main__":
    unittest.main()
