import math
from color import Color


class Layer:
    """Class that stores the pixel data of an image layer"""

    from _simple_transformations import flip_horizontal_axis
    from _simple_transformations import flip_vertical_axis
    from _simple_transformations import rotate_counter_clockwise

    from _advanced_transformations import color_at
    from _advanced_transformations import interpolate_bilinear
    from _advanced_transformations import interpolate_nearest_neighbor
    from _advanced_transformations import rotate_same_size
    from _advanced_transformations import scale_backward
    from _advanced_transformations import scale_forward
    from _advanced_transformations import translate
    from _advanced_transformations import get_in_place_matrix
    from _advanced_transformations import get_expanded_matrix
    from _advanced_transformations import rotate_expand

    def __init__(self, width: int, height: int, offset_x=0, offset_y=0):
        """Store the constructor arguments"""
        self.width, self.height = width, height
        self.offset_x, self.offset_y = offset_x, offset_y
        self.pixels = [0, 0, 0] * self.width * self.height

    def generate_histogram(self):
        layer = Layer(256, 100, 0, 0)

        histogram = [0] * 256
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                if grayscale >= 256:
                    print("Stop")
                histogram[grayscale] += 1

        max = 0
        for h in histogram:
            if h > max:
                max = h

        # Now normalize the histogram
        histogram_max = 100
        for i in range(256):
            h = histogram[i]
            h /= max
            h *= histogram_max
            histogram[i] = h

        # Draw the histogram
        for i in range(256):
            for j in range(math.floor(histogram[i])):
                layer.set_pixel(i, histogram_max - j-1, (255, 255, 255))

        return layer

    def generate_row_histogram(self):
        layer = Layer(self.width, 25, 0, 0)

        histogram = [0] * self.width
        for x in range(self.width):
            sum = 0
            for y in range(self.height):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                sum += grayscale
            histogram[x] = sum

        max = 0
        for h in histogram:
            if h > max:
                max = h

        # Now normalize the histogram
        histogram_max = 25
        for i in range(len(histogram)):
            h = histogram[i]
            h /= max
            h *= histogram_max
            histogram[i] = h

        # Draw the histogram
        for i in range(self.width):
            for j in range(math.floor(histogram[i])):
                layer.set_pixel(i, j, (255, 255, 255))

        return layer

    def generate_column_histogram(self):
        layer = Layer(25, self.height, 0, 0)

        histogram = [0] * self.height
        for y in range(self.height):
            sum = 0
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                sum += grayscale
            histogram[y] = sum

        max = 0
        for h in histogram:
            if h > max:
                max = h

        # Now normalize the histogram
        histogram_max = 25
        for i in range(len(histogram)):
            h = histogram[i]
            h /= max
            h *= histogram_max
            histogram[i] = h

        # Draw the histogram
        for i in range(self.height):
            for j in range(math.floor(histogram[i])):
                layer.set_pixel(j, i, (255, 255, 255))

        return layer

    def brighten(self, amount):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)

                new_pixel = (pixel[0] + amount, pixel[1] +
                             amount, pixel[2] + amount)

                self.set_pixel(x, y, new_pixel)

    def add_contrast(self, amount):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = (pixel[0] + pixel[1] + pixel[2])/3
                to_add = amount
                if grayscale < 128:
                    to_add *= -1

                new_pixel = (pixel[0] + to_add, pixel[1] +
                             to_add, pixel[2] + to_add)

                self.set_pixel(x, y, new_pixel)

    def add_contrast2(self, amount):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = (pixel[0] + pixel[1] + pixel[2])/3
                offset = grayscale - 128
                offset *= amount
                offset += 128
                offset = math.floor(offset - grayscale)

                new_pixel = (pixel[0] + offset, pixel[1] +
                             offset, pixel[2] + offset)

                self.set_pixel(x, y, new_pixel)

    def auto_tune_brightness(self):
        sum = 0
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = (pixel[0] + pixel[1] + pixel[2])/3
                sum += grayscale - 128
        average_offset = -math.floor(sum // (self.height * self.width))
                
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                
                new_pixel = (pixel[0] + average_offset, pixel[1] +
                             average_offset, pixel[2] + average_offset)

                self.set_pixel(x, y, new_pixel)

    def auto_tune_everything(self):
        histogram = [0] * 256
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                if grayscale >= 256:
                    print("Stop")
                histogram[grayscale] += 1
        total_pixels = self.width * self.height
        # How far should we scale so that X% of the pixels span 0 to 255?
        outlier_count = total_pixels * .025
        sum_dark = 0
        sum_light = 0
        offset_index_dark = 0
        offset_index_light = 255
        
        while True:
            dark_index = offset_index_dark
            sum_dark += histogram[dark_index] 
            offset_index_dark += 1
            if sum_dark > outlier_count:
                break
        while True:
            light_index = offset_index_light
            sum_light += histogram[light_index] 
            offset_index_light -= 1
            if sum_light > outlier_count:
                break
        
        desired_width = offset_index_light - offset_index_dark
        average_offset = desired_width - 128
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                off = (grayscale - dark_index) * 255/light_index 
                delta = -math.floor(grayscale - off)
                new_pixel = (pixel[0] + delta, pixel[1] +
                             delta, pixel[2] + delta)

                self.set_pixel(x, y, new_pixel)

    def auto_tune_contrast(self):
        histogram = [0] * 256
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.get_pixel(x, y)
                grayscale = math.floor((pixel[0] + pixel[1] + pixel[2])/3)
                if grayscale >= 256:
                    print("Stop")
                histogram[grayscale] += 1
        total_pixels = self.width * self.height
        # How far should we scale so that X% of the pixels span 0 to 255?
        outlier_count = total_pixels * .025
        sum = 0
        offset_index = 0
        cont = True
        while cont:
            dark_index = offset_index
            light_index = 255 - offset_index
            sum += histogram[dark_index] + histogram[light_index]
            offset_index += 1
            if sum > outlier_count:
                break
        desired_width = 255 - (offset_index*2)
        scale = 255 / desired_width
        self.add_contrast2(scale)

        

    def set_pixel(self, x, y, color) -> None:
        """Set a pixel in the layer buffer"""
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print("Bad set_pixel coordinate.")
            return

        new_color = (
            min(255, max(0, color[0]))//1,
            min(255, max(0, color[1]))//1,
            min(255, max(0, color[2]))//1)
        self.pixels[y*self.width+x] = new_color

    def get_pixel(self, x: int, y: int):
        """ Given x and y, return the color of the pixel"""
        index = self.pixelIndex(x, y)
        return self.pixels[index]

    def pixelIndex(self, x: int, y: int) -> int:
        """Given x and y, find the index in our linear array."""
        index = y*self.width + x
        return index
