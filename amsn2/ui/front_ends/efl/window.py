
from constants import WIDTH, HEIGHT, THEME_FILE, WM_NAME, WM_CLASS
import evas
import elementary

from amsn2.ui import base
from amsn2.views import MenuItemView

class aMSNWindow(elementary.Window, base.aMSNWindow):
    def __init__(self, amsn_core):
        self._amsn_core = amsn_core
        elementary.Window.__init__(self, "aMSN", elementary.ELM_WIN_BASIC)
        self.resize(WIDTH, HEIGHT)
        self.on_key_down_add(self._on_key_down)
        self.fullscreen = False
        self.name_class_set = (WM_NAME, WM_CLASS)

        self._bg = elementary.Background(self)
        self.resize_object_add(self._bg)
        self._bg.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                      evas.EVAS_HINT_EXPAND)
        self._bg.show()

        self._ly = elementary.Layout(self)
        self._ly.file_set(THEME_FILE, "amsn2/win")
        self.resize_object_add(self._ly)
        self._ly.size_hint_weight_set(evas.EVAS_HINT_EXPAND,
                                      evas.EVAS_HINT_EXPAND)
        self._ly.size_hint_align_set(evas.EVAS_HINT_FILL,
                                     evas.EVAS_HINT_FILL)
        self._edje = self._ly.edje_get()
        self._ly.show()

        self._tb = None

    def block(self, block):
        if block:
            self._edje.signal_emit("blocker,enable", "")
        else:
            self._edje.signal_emit("blocker,disable", "")

    def child_set(self, child):
        self._ly.content_set("content", child)
        child.size_hint_weight_set(1, 1)

    child = property(fset=child_set)

    @property
    def _evas(self):
        return self.evas_get()

    def hide(self):
        pass

    def set_title(self, text):
        self.title_set(text)

    def set_menu(self, mv):
        if self._tb:
            self._tb.delete()
        if mv is None:
            return
        self._tb = elementary.Toolbar(self)
        self._tb.homogenous = False
        self._tb.align = 0.0
        self._tb.size_hint_weight_set(0.0, 0.0)
        self._tb.size_hint_align_set(evas.EVAS_HINT_FILL, 0.0)
        self._ly.content_set("menubar", self._tb)
        for item in mv.items:
            if item.type is MenuItemView.CASCADE_MENU:
                ic = None
                if item.icon:
                    #TODO
                    pass
                mi = self._tb.item_add(ic, item.label)
                mi.menu_set(True)
                tm = mi.menu_get()
                create_menu_from_menuview(item.items, tm, None)
        self._tb.menu_parent_set(self)
        self._tb.show()

    def toggle_menu(self):
        if self._tb:
            #TODO
            if True:
                self._tb.hide()
            else:
                self._tb.show()

    def _on_key_down(self, obj, event):
        pass

def create_menu_from_menuview(items, menu, parent):
    pass
    for item in items:
        if item.type is MenuItemView.CASCADE_MENU:
            ic = None
            if item.icon:
                #TODO
                pass
            mi = menu.item_add(parent, item.label, ic)
            create_menu_from_menuview(item.items, menu, mi)
        elif item.type is MenuItemView.COMMAND:
            ic = None
            if item.icon:
                #TODO
                pass
            cb = None
            if item.command:
                def _cb(menu, it):
                    item.command()
                cb = _cb
            menu.item_add(parent, item.label, ic, cb)
        elif item.type is MenuItemView.SEPARATOR:
            menu.item_separator_add(parent)
