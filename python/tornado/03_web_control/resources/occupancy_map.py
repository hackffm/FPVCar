import os

from PIL import Image, ImageDraw


class OccupancyMap:

    def __init__(self, free_thresh=19, height=1000, image='image.png', negate=0, occupied_thresh=90,
                 origin=[10.0, 10.0, 10.0],resolution='0.01', width=1000):

        self.free_thresh = free_thresh
        self.image = image
        self.negate = negate
        self.occupied_thresh = occupied_thresh
        self.origin = origin
        self.resolution = resolution

        # colour values
        self.free = 254
        self.occupied = 0
        self.unknown = 205

        # map dimensions
        self.height = height
        self.width = width

        self.image = Image.new('L', (self.width, self.height), self.unknown)

    def add_free(self, pos_x, pos_y):
        draw = ImageDraw.Draw(self.image)
        draw.point((pos_x, pos_y), fill=self.free)

    def add_occupied(self, pos_x, pos_y):
        draw = ImageDraw.Draw(self.image)
        draw.point((pos_x, pos_y), fill=self.occupied)

    def add_unknown(self, pos_x, pos_y):
        draw = ImageDraw.Draw(self.image)
        draw.point((pos_x, pos_y), fill=self.unknown)

    def file_exists(self, path_file):
        if not os.path.isfile(path_file):
            return False
        return True

    def img_load(self, image_path):
        if self.file_exists(image_path):
            self.image = Image.open(image_path)
            return self.image
        else:
            return 'failed finding ' + image_path
