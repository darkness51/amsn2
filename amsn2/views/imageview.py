class ImageView(object):
    """
        Known resource_type are:
            - Filename
            - Theme
            - None
    """

    FILENAME = "Filename"
    THEME = "Theme"

    def __init__(self, resource_type=None, value=None):
        """
        @type resource_type: str
        @type value: object
        """
        self.imgs = []
        if resource_type is not None and value is not None:
            self.load(resource_type, value)

    def load(self, resource_type, value):
        """
        @type resource_type: str
        @type value: object
        """
        self.imgs = [(resource_type, value)]

    def append(self, resource_type, value):
        """
        @type resource_type: str
        @type value: object
        """
        self.imgs.append((resource_type, value))

    def prepend(self, resource_type, value):
        """
        @type resource_type: str
        @type value: object
        """
        self.imgs.insert(0, (resource_type, value))

    def clone(self):
        img = ImageView()
        img.imgs = self.imgs[:]
        return img

    def append_imageview(self, iv):
        """
        @type iv: L{amsn2.views.imageview.ImageView} 
        """
        self.imgs.extend(iv.imgs)

    def prepend_imageview(self, iv):
        """
        @type iv: L{amsn2.views.imageview.ImageView}
        """
        self.imgs = iv.imgs[:].extend(self.imgs)

    def reset(self):
        self.imgs = []

