from layer import Layer
from PIL import Image


class Container:
    """A list of layer objects

    Args:
      width (int): The width of the container
      height (int): The height of the container
    """

    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.image = Image.new("RGB", (width, height))
        self.buffer = self.image.load()
        self.layers = []

    def remove_layer_index(self, index: int):
        del self.layers[index]
        return self

    def add_layer(self, layer: Layer, offset_x=0, offset_y=0):
        """Add a layer to the container

        Args:
          layer (Layer): The layer to add to the container
        """
        layer.parent = self
        layer.offset_x = offset_x
        layer.offset_y = offset_y

        self.layers.append(layer)
        return self

    def resize(self, width, height):
        self.width, self.height = width, height
        self.image = Image.new("RGB", (width, height))
        self.buffer = self.image.load()
        return self

    def expand_size(self, dx, dy):
        self.width += dx
        self.height += dy
        return self

    def pack(self):
        """ 
        Loop through all the layers and make this container big enough
        for all of them.
        """

        max_x = 0
        max_y = 0
        for layer in self.layers:
            desired_x = layer.width + layer.offset_x
            desired_y = layer.height + layer.offset_y
            if  desired_x > max_x:
                max_x = desired_x
            if desired_y > max_y:
                max_y = desired_y
        self.width = max_x
        self.height = max_y
        return self

    def save(self, filename):
        """
        Rasterize and save the layers

        Step 1: Rasterize all layers to this container's buffer
        Step 2: Save that buffer to the filesystem

        Args:
          filename (string): The filename to save to
        """

        self.image = Image.new("RGB", (self.width, self.height))
        self.buffer = self.image.load()
        for layer in self.layers:
            ox = layer.offset_x
            oy = layer.offset_y
            if oy < 0:
                oy = self.height + oy
            if ox < 0:
                ox = self.width + ox
            for y in range(min(layer.height, self.height)):
                for x in range(min(layer.width, self.width)):
                    color = layer.get_pixel(x, y)
                    planned_x, planned_y = x+ox, y+oy
                    if planned_x >= self.width or planned_x < 0:
                        print("You are out of bounds in x")
                        continue
                    if planned_y >= self.height or planned_y < 0:
                        print("You are out of bounds in y")
                        continue
                    self.buffer[planned_x, planned_y] = color
        self.image.save(filename, "png")
