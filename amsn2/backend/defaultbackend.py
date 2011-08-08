
from amsn2.core.config import aMSNConfig
import os
import defaultaccountbackend

"""ElementTree independent from the available distribution"""
try:
    from xml.etree.cElementTree import *
except ImportError:
    try:
        from cElementTree import *
    except ImportError:
        from elementtree.ElementTree import *

class defaultbackend(defaultaccountbackend.defaultaccountbackend):
    """
    Backend used to save the config on the home directory of the user.
    """

    def __init__(self):
        defaultaccountbackend.defaultaccountbackend.__init__(self)

    def save_config(self, account, config):
        """
        @type account: L{amsn2.core.account_manager.aMSNAccount}
        @type config: L{amsn2.core.config.aMSNConfig}
        """
        #TODO: improve
        root_section = Element("aMSNConfig")
        for e in config._config:
            val = config._config[e]
            elmt = SubElement(root_section, "entry",
                              type=type(val).__name__,
                              name=str(e))
            elmt.text = str(val)

        accpath = os.path.join(self.accounts_dir, self._get_dir(account.view.email),
                               "config.xml")
        xml_tree = ElementTree(root_section)
        xml_tree.write(accpath, encoding='utf-8')

    def load_config(self, account):
        """
        @type account: L{amsn2.core.account_manager.aMSNAccount}
        """
        c = aMSNConfig()
        c.set_key("ns_server", "messenger.hotmail.com")
        c.set_key("ns_port", 1863)

        configpath = os.path.join(self.accounts_dir,
                                  self._get_dir(account.view.email),
                                  "config.xml")
        
        configfile = None
        try:
            configfile = file(configpath, "r")
        except IOError:
            return c

        root_tree = ElementTree(file=configfile)
        configfile.close()
        config = root_tree.getroot()
        if config.tag == "aMSNConfig":
            lst = config.findall("entry")
            for elmt in lst:
                if elmt.attrib['type'] == 'int':
                    c.set_key(elmt.attrib['name'], int(elmt.text))
                else:
                    c.set_key(elmt.attrib['name'], elmt.text)
        return c

    def clean(self):
        pass

