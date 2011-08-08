from amsn2.views.keybindingview import KeyBindingView

class MenuItemView(object):
    CASCADE_MENU = "cascade"
    CHECKBUTTON = "checkbutton"
    RADIOBUTTON = "radiobutton"
    RADIOBUTTONGROUP = "radiobuttongroup"
    SEPARATOR = "separator"
    COMMAND = "command"

    def __init__(self, type, label = None, icon = None, accelerator = None,
                 radio_value = None, checkbox_value = False, disabled = False,  command = None):
        """ Create a new MenuItemView
        @type type: str defined in L{amsn2.views.menuview.MenuItemView}
        @param type: the type of item, can be cascade, checkbutton, radiobutton,
        radiogroup, separator or command
        @type label: str
        @param label: the label for the item, unused for separator items
        @type icon: object
        @param icon: an optional icon to show next to the menu item, unused for separator items
        @type accelerator: L{amsn2.views.keybindingview.KeyBindingView}
        @param accelerator: the accelerator (KeyBindingView) to access this item.
                       If None, an '&' preceding a character of the menu label will set that key with Ctrl- as an accelerator
        @type radio_value: object
        @param radio_value: the value to set when the radiobutton is enabled
        @type checkbox_value: bool
        @param checkbox_value: whether the checkbox/radiobutton is set or not
        @type disabled: bool
        @param disabled: true if the item's state should be disabled
        @type command: function
        @param command: the command to call for setting the value for checkbutton and radiobutton items, or the command in case of a 'command' item

        @todo: dynamic menus (use 'command' in CASCADE_MENU)
        """

        if ((type is MenuItemView.SEPARATOR and
             (label is not None or
              icon is not None or
              accelerator is not None or
              radio_value is not None or
              checkbox_value is not False or
              disabled is True or
              command is not None)) or
            (type is MenuItemView.CHECKBUTTON and
              command is None) or
            (type is MenuItemView.RADIOBUTTON and
              command is None) or
            (type is MenuItemView.RADIOBUTTONGROUP and 
             (command is not None or
              checkbox_value is not False or
              label is not None)) or
            (type is MenuItemView.COMMAND and
             (radio_value is not None or
              checkbox_value is not False or
              command is None )) or
            (type is MenuItemView.CASCADE_MENU and
             (radio_value is not None or
              checkbox_value is not False or
              icon is not None or
              command is not None))):
            raise ValueError

        new_label = label
        if accelerator is None and label is not None:
            done = False
            new_label = ""
            while not done:
                part = label.partition('&')
                new_label += part[0]
                if part[1] == '&':
                    if part[2].startswith('&'):
                        new_label += '&'
                        label = part[2][1:]
                    elif len(part[2]) > 0:
                        if accelerator is None:
                            accelerator = KeyBindingView(key = part[2][0], control = True)
                        label = part[2]
                    else:
                        done = True
                else:
                    done = True


        self.type = type
        self.label = new_label
        self.icon = icon
        self.accelerator = accelerator
        self.radio_value = radio_value
        self.disabled = disabled
        self.command = command
        self.items = []

    def add_item(self, item):
        self.items.append(item)

class MenuView(object):
    """
    Base class for a menu.
    If subclassed allows a menu, or part of it, to be updated when the items are requested.
    """
    def __init__(self):
        self._fixed_items = []

    def add_item(self, item):
        """
        @type item: L{amsn2.views.menuview.MenuItemView}
        """
        self._fixed_items.append(item)

    def _get_items(self):
        self.create_var_items()
        return self._fixed_items + self._var_items

    items = property(_get_items)
    def create_var_items(self):
        """
        Override this method to have a MenuView that can
        change its elements depending on amsn2's status
        """
        self._var_items = []

