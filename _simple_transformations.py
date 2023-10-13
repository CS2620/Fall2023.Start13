def flip_horizontal_axis(self):
    """ Flip the image about the horizontal axis"""
    new_pixels = [0, 0, 0] * self.width * self.height
    for y in range(self.height):
        for x in range(self.width):
            from_pixel_x = x
            from_pixel_y = self.height - y - 1
            from_pixel_index = self.pixelIndex(from_pixel_x, from_pixel_y)
            from_pixel = self.pixels[from_pixel_index]

            new_pixel_index = self.pixelIndex(x, y)

            new_pixels[new_pixel_index] = from_pixel
    self.pixels = new_pixels

def flip_vertical_axis(self):
    """ Flip the image about the vertical axis"""
    new_pixels = [0, 0, 0] * self.width * self.height
    for y in range(self.height):
        for x in range(self.width):
            from_pixel_x = self.width - x - 1
            from_pixel_y = y
            from_pixel_index = self.pixelIndex(from_pixel_x, from_pixel_y)
            from_pixel = self.pixels[from_pixel_index]

            new_pixel_index = self.pixelIndex(x, y)

            new_pixels[new_pixel_index] = from_pixel
    self.pixels = new_pixels

def rotate_counter_clockwise(self):
    """ Rotate the image 90 degrees in the counter-clockwise direction."""
    new_pixels = [0, 0, 0] * self.width * self.height
    new_width = self.height
    new_height = self.width
    for y in range(self.height):
        for x in range(self.width):
            to_pixel_x = y
            to_pixel_y = -x + self.width - 1
            to_pixel_index = to_pixel_y*new_width + to_pixel_x
            from_index = self.pixelIndex(x, y)
            from_pixel = self.pixels[from_index]

            new_pixels[to_pixel_index] = from_pixel
    self.pixels = new_pixels
    self.width = new_width
    self.height = new_height
