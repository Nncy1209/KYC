import easyocr
import numpy as np
from PIL import Image


class OCRService:

    def __init__(self):
        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    def extract_text(self, image):

        if isinstance(image, Image.Image):
            image = np.array(image)

        result = self.reader.readtext(image)

        text = []

        for item in result:
            text.append(item[1])

        return "\n".join(text)