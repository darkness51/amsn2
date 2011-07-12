import os.path

class Skin(object):
    def __init__(self, core, path):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        @type path: str
        """

        self._path = path
        pass

    def key_get(self, key, default):
        """
        @type key: str
        @type default: str
        """
        pass

    def key_set(self, key, value):
        """
        @type key: str
        @type value: str
        """
        pass



class SkinManager(object):
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """
        self._core = core
        self.skin = Skin(core, "skins")

    def skin_set(self, name):
        """
        @type name: str
        """
        self.skin = Skin(self._core, os.path.join("skins", name))
        pass

    def get_skins(self, path):
        """
        @type path: str
        """
        pass
