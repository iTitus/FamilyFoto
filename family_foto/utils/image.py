import os

from PIL import Image
from resizeimage.resizeimage import resize_width

from family_foto.config import BaseConfig


def resize(path: str, filename: str, height: int, width: int):
    with open(path, 'r+b') as file:
        with Image.open(file) as image:
            cover = resize_width(image, width)
            if not os.path.exists(BaseConfig.RESIZED_DEST):
                os.mkdir(BaseConfig.RESIZED_DEST)
            save_path = f'{BaseConfig.RESIZED_DEST}/{width}_{height}_{filename}'
            cover.save(save_path, image.format)
            image.close()
        file.close()
    return save_path
