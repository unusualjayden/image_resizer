import os.path

import requests
from PIL import Image


class ImageResizer:
    def __init__(self, path):
        self.path = os.path.join('./media', 'uploads', os.path.basename(path))
        self.image = Image.open(self.path)
        self.size = self.image.size

    def get_image_url(self):
        return self.path[1:]

    def get_name_to_new_image(self, size):
        (name, extension) = os.path.basename(self.path).split('.')
        return f'{name}_{size[0]}x{size[1]}.{extension}'

    def get_path_to_new_image(self, size):
        return os.path.join('./media', 'uploads', self.get_name_to_new_image(size))

    def get_extension(self):
        return os.path.basename(self.path).split('.')[1]

    def check_if_resizing_exists(self, size):
        return os.path.exists(self.get_path_to_new_image(size))

    def resize(self, new_size):
        old_size = [float(x) for x in self.size]

        if new_size[0] == '' and new_size[1] == '':
            return self
        elif new_size[0] == '':
            k = float(new_size[1]) / float(old_size[1])
        else:
            k = float(new_size[0]) / float(old_size[0])

        new_size = (int(k * float(old_size[0])), int(k * float(old_size[1])))

        if self.check_if_resizing_exists(new_size):
            return ImageResizer(self.get_name_to_new_image(new_size))

        new_path = self.get_path_to_new_image(new_size)

        self.image = self.image.resize(new_size)
        self.image.save(new_path)
        self.size = new_size
        self.path = new_path
        return self


def image_download_handler(url, name):
    r = requests.get(url)
    extension = r.headers.get('Content-Type').split('/')[1]
    with open(os.path.join('./media', 'uploads', f'{name}.jpg'), 'wb') as out_file:
        out_file.write(r.content)
    return os.path.join('uploads', f'{name}.{extension}')
