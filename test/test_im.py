import unittest
from os import path
from src import im
from io import BytesIO

THUMB_LENGTH = str(290)

def with_image(name, consumer):
    p = path.dirname(__file__) + "/fixture/images/" + name
    with open(p, "rb") as f:
        image = BytesIO(f.read())
        consumer((image, name))

class ImageMagickTestCase(unittest.TestCase):
    def setUp(self):
        self.app = im.app.test_client()

    def tearDown(self):
        None

    def test_ping(self):
        response = self.app.get("/ping")
        self.assertEqual(response.data, b"pong")

    def test_resize_with_valid_params(self):
        def action(image):
            params = dict(
                width=THUMB_LENGTH,
                height=THUMB_LENGTH,
                data=image,
            )
            response = self.request_resize(params)
            self.assertEqual(response.status_code, 200)

        with_image("kosys.png", action)

    def test_resize_without_width(self):
        def action(image):
            params = dict(height=THUMB_LENGTH, data=image)
            response = self.request_resize(params)
            self.assertEqual(response.status_code, 400)

        with_image("kosys.png", action)

    def test_resize_without_height(self):
        def action(image):
            params = dict(width=THUMB_LENGTH, data=image)
            response = self.request_resize(params)
            self.assertEqual(response.status_code, 400)

        with_image("kosys.png", action)

    def test_resize_without_data(self):
        params = dict(width=THUMB_LENGTH, height=THUMB_LENGTH)
        response = self.request_resize(params)
        self.assertEqual(response.status_code, 400)

    def request_resize(self, params):
        return self.app.post("/resize",
            content_type='multipart/form-data',
            data=params
        )
if __name__ == "__main__":
    unittest.main()
