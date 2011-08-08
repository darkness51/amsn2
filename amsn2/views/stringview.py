# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2008 Dario Freddi <drf54321@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import cgi

class StringView (object):
    TEXT_ELEMENT = "text"
    COLOR_ELEMENT = "color"
    BACKGROUND_ELEMENT = "bgcolor"
    IMAGE_ELEMENT = "image"
    OPEN_TAG_ELEMENT = "tag"
    CLOSE_TAG_ELEMENT = "-tag"
    ITALIC_ELEMENT = "italic"
    BOLD_ELEMENT = "bold"
    UNDERLINE_ELEMENT = "underline"
    FONT_ELEMENT = "font"
    SMILEY_ELEMENT = "smiley"

    # padding ?

    class StringElement(object):
        def __init__(self, type, value):
            """
            @type type: str defined in L{amsn2.views.stringview.StringView}
            @type value: str
            """
            self._type = type
            self._value = value

        def get_type(self):
            return self._type

        def get_value(self):
            return self._value

    class ColorElement(StringElement):
        def __init__(self, color):
            """
            @type color: object
            """
            StringView.StringElement.__init__(self, StringView.COLOR_ELEMENT, color)
    class BackgroundColorElement(StringElement):
        def __init__(self, color):
            """
            @type color: object
            """
            StringView.StringElement.__init__(self, StringView.BACKGROUND_ELEMENT, color)
    class TextElement(StringElement):
        def __init__(self, text):
            """
            @type text: str
            """
            StringView.StringElement.__init__(self, StringView.TEXT_ELEMENT, text)
    class ImageElement(StringElement):
        def __init__(self, image):
            """
            @type image: object
            """
            StringView.StringElement.__init__(self, StringView.IMAGE_ELEMENT, image)
    class OpenTagElement(StringElement):
        def __init__(self, tag):
            """
            @type tag: str
            """
            StringView.StringElement.__init__(self, StringView.OPEN_TAG_ELEMENT, tag)
    class CloseTagElement(StringElement):
        def __init__(self, tag):
            """
            @type tag: str
            """
            StringView.StringElement.__init__(self, StringView.CLOSE_TAG_ELEMENT, tag)
    class FontElement(StringElement):
        def __init__(self, font):
            """
            @type font: object
            """
            StringView.StringElement.__init__(self, StringView.FONT_ELEMENT, font)
    class BoldElement(StringElement):
        def __init__(self, bold):
            """
            @type bold: bool
            """
            StringView.StringElement.__init__(self, StringView.BOLD_ELEMENT, bold)
    class ItalicElement(StringElement):
        def __init__(self, italic):
            """
            @type italic: bool
            """
            StringView.StringElement.__init__(self, StringView.ITALIC_ELEMENT, italic)
    class UnderlineElement(StringElement):
        def __init__(self, underline):
            """
            @type underline: bool
            """
            StringView.StringElement.__init__(self, StringView.UNDERLINE_ELEMENT, underline)
    class SmileyElement(StringElement):
        def __init__(self, (image, alt)):
            """
            @type image: object
            @type alt: str 
            """
            StringView.StringElement.__init__(self, StringView.SMILEY_ELEMENT, (image, alt))

    def __init__(self, default_background_color = None, default_color = None, default_font = None):
        """
        @type default_background_color: object
        @type default_color: object
        @type default_font: object
        """
        self._elements = []
        from amsn2.core import aMSNCore
        self._core = aMSNCore()

        self._default_background_color = default_background_color
        self._default_color = default_color
        self._default_font = default_font

        if default_color is not None:
            self.reset_color()
        if default_background_color is not None:
            self.reset_background_color()
        if default_font is not None:
            self.reset_font()

    def append(self, type, value):
        """
        @type type: str defined in L{amsn2.views.stringview.StringView}
        @type value: str
        """
        self._elements.append(StringView.StringElement(type, value))

    def append_smiley(self, image, alt):
        """
        @type image: object
        @type alt: str
        """
        self._elements.append(StringView.SmileyElement((image, alt)))
    def append_stringview(self, strv):
        """
        @type strv: L{amsn2.views.stringview.StringView}
        """
        #TODO: default (bg)color
        self._elements.extend(strv._elements)
    def append_text(self, text):
        """
        @type text: str
        """
        self._elements.append(StringView.TextElement(text))
    def append_image(self, image):
        """
        @type image: object
        """
        self._elements.append(StringView.ImageElement(image))
    def set_color(self, color):
        """
        @type color: object
        """
        self._elements.append(StringView.ColorElement(color))
    def set_background_color(self, color):
        """
        @type color: object
        """
        self._elements.append(StringView.BackgroundColorElement(color))
    def set_font(self, font):
        """
        @type font: object
        """
        self._elements.append(StringView.FontElement(font))
    def open_tag(self, tag):
        """
        @type tag: str
        """
        self._elements.append(StringView.OpenTagElement(tag))
    def close_tag(self, tag):
        """
        @type tag: str
        """
        self._elements.append(StringView.CloseTagElement(tag))

    def set_bold(self):
        self._elements.append(StringView.BoldElement(True))
    def unset_bold(self):
        self._elements.append(StringView.BoldElement(False))
    def set_italic(self):
        self._elements.append(StringView.ItalicElement(True))
    def unset_italic(self):
        self._elements.append(StringView.ItalicElement(False))
    def set_underline(self):
        self._elements.append(StringView.UnderlineElement(True))
    def unset_underline(self):
        self._elements.append(StringView.UnderlineElement(False))

    def reset(self):
        self._elements = []
    def reset_color(self):
        self.set_color(self._default_color)
    def reset_background_color(self):
        self.set_background_color(self._default_background_color)
    def reset_font(self):
        self.set_font(self._default_font)

    def parse_default_smileys(self):
        new_stringview = self
        theme_manager = self._core._theme_manager
        smiley_manager = self._core._smiley_manager
        for shortcut in smiley_manager.default_smileys_shortcuts:
            temp_stringview = StringView()
            for element in new_stringview._elements:
                if element.get_type() == StringView.TEXT_ELEMENT:
                    finished = False
                    text = element.get_value()
                    while not finished:
                        pos = text.lower().find(shortcut.lower())
                        if (pos == -1):
                            finished = True
                            temp_stringview.append_text(text)
                        else:
                            temp_stringview.append_text(text[:pos])
                            temp_stringview.append_smiley(theme_manager.get_smiley(smiley_manager.default_smileys_shortcuts[shortcut])[1], shortcut) #the [1] is because the theme manager returns a tuple
                            text = text[pos+len(shortcut):]
                else:
                    temp_stringview.append(element.get_type(), element.get_value())
            new_stringview = temp_stringview
        return new_stringview

    def to_HTML_string(self):
        """ This method returns a formatted html string with all
        the data in the stringview """
        out = ""
        for x in self._elements:
            if x.get_type() == StringView.TEXT_ELEMENT:
                out += cgi.escape(x.get_value())
            elif x.get_type() == StringView.ITALIC_ELEMENT:
                if x.get_value() == True:
                    out += "<i>"
                else:
                    out += "</i>"
            elif x.get_type() == StringView.BOLD_ELEMENT:
                if x.get_value() == True:
                    out += "<b>"
                else:
                    out += "</b>"
            elif x.get_type() == StringView.IMAGE_ELEMENT:
                out += "<img src=\""+x.get_value()+"\" />"
            elif x.get_type() == StringView.SMILEY_ELEMENT:
                out += "<img src=\""+x.get_value()[0]+"\" />"
            elif x.get_type() == StringView.UNDERLINE_ELEMENT:
                if x.get_value() == True:
                    out += "<u>"
                else:
                    out += "</u>"
        return out

    def get_tag(self, tagname):
        """
        @type tagname: str
        """

        for i in range(len(self._elements)):
            e = self._elements[i]
            if e.get_type() == StringView.OPEN_TAG_ELEMENT and e.get_value() == tagname:
                begin = i+1
                break

        sv = StringView()

        #if begin is None, raise exception?
        if begin is not None:
            e = self._elements[begin]

            while not (e.get_type() == StringView.CLOSE_TAG_ELEMENT and e.get_value() == tagname):
                sv.append(e.get_type(), e.get_value())
                begin += 1
                e = self._elements[begin]

        return sv

    def __unicode__(self):
        out = u""
        for x in self._elements:
            if x.get_type() == StringView.TEXT_ELEMENT:
                out += x.get_value()
        return out

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        out = "{"
        for x in self._elements:
            out += "[" + x.get_type() + "=" + str(x.get_value()) + "]"

        out += "}"
        return out

