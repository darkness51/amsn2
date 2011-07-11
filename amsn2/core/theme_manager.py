# -*- coding: utf-8 -*-
#===================================================
#
# theme_manager.py - This file is part of the amsn2 package
#
# Copyright (C) 2008  Wil Alvarez <wil_alejandro@yahoo.com>
#
# This script is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later
# version.
#
# This script is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or 
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
# for more details.
#
# You should have received a copy of the GNU General Public License along with 
# this script (see COPYING); if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#===================================================

import os

class aMSNThemeManager:
    def __init__(self, core):
        """
        @type core: L{amsn2.core.amsn.aMSNCore}
        """
        self._core = core
        self._buttons = {}
        self._statusicons = {}
        self._displaypic = {}
        self._emblems = {}

        self.load()

    def __get(self, var, key):
        """
        @type var: dict
        @type key: str
        """
        # TODO: evaluate if should be returned None when key is not valid
        if key in var.keys():
            return var[key]
        else:
            return (None, None)

    def load(self):
        # Here aMSNThemeManager should read user's files to know what theme
        # will be loaded to each aspect
        self._buttons = aMSNButtonLoader().load('default')
        self._statusicons = aMSNStatusIconLoader().load('default')
        self._displaypic = aMSNDisplayPicLoader().load('default')
        self._emblems = aMSNEmblemLoader().load('default')
        self._smileys = aMSNSmileyLoader().load('default')

    def get_value(self, key):
        """
        @type key: str
        """
        if (key.startswith('button_')):
            return self.get_button(key)
        elif (key.startswith('buddy_')):
            return self.get_statusicon(key)
        elif (key.startswith('dp_')):
            return self.get_dp(key)
        elif (key.startswith('emblem_')):
            return self.get_emblem(key)
        elif (key.startswith('smiley_')):
            return self.get_smiley(key)
        else:
            # TODO: This should raise a exception
            return (None, None)

    def get_button(self, key):
        """
        @type key: str
        """
        return self.__get(self._buttons, key)

    def get_statusicon(self, key):
        """
        @type key: str
        """
        return self.__get(self._statusicons, key)

    def get_dp(self, key):
        """
        @type key: str
        """
        return self.__get(self._displaypic, key)

    def get_emblem(self, key):
        """
        @type key: str
        """
        return self.__get(self._emblems, key)

    def get_smiley(self, key):
        """
        @type key: str
        """
        return self.__get(self._smileys, key)

class aMSNGenericLoader:
    def __init__(self, basedir):
        """
        @type basedir: str
        """
        self._theme = 'default'
        self._basedir = os.path.join("amsn2", "themes", basedir)
        self._defaultdir = os.path.join(self._basedir, "default")
        # Keys holds a pair (key,filename)
        # Should be initialized after creating the class
        self._keys = []
        self._dict = {}

    def load(self, theme='default'):
        """
        @type theme: str
        """
        self.theme = theme
        self._theme_dir = os.path.join(self._basedir, theme)

        for key in self._keys.keys():
            image = self._keys[key]
            filepath = os.path.join(self._theme_dir, image)

            # Verificating
            if (not os.path.isfile(filepath)):
                filepath = os.path.join(self._defaultdir, image)

            self._dict[key] = ("Filename", filepath)

        return self._dict

class aMSNButtonLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "buttons")
        self._keys = {
            'button_nudge': 'nudge.png',
            'button_smile': 'smile.png',
        }

class aMSNStatusIconLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "status_icons")
        self._keys = {
            'buddy_online': 'online.png',
            'buddy_away': 'away.png',
            'buddy_brb': 'away.png',
            'buddy_idle': 'away.png',
            'buddy_lunch': 'away.png',
            'buddy_busy': 'busy.png',
            'buddy_phone': 'phone.png',
            'buddy_offline': 'offline.png',
            'buddy_hidden': 'offline.png',
            'buddy_blocked': 'blocked.png',
            'buddy_blocked_off': 'blocked_off.png',
            'buddy_webmsn': 'webmsn.png',
        }

class aMSNDisplayPicLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "displaypic")
        self._keys = {
            'dp_amsn': 'amsn.png', 
            'dp_female': 'female.png',
            'dp_loading': 'loading.png',
            'dp_male': 'male.png',
            'dp_nopic': 'nopic.png',
        }

class aMSNEmblemLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "emblems")
        self._keys = {
            'emblem_online': 'plain_emblem.png',
            'emblem_away': 'away_emblem.png',
            'emblem_brb': 'away_emblem.png',
            'emblem_idle': 'away_emblem.png',
            'emblem_lunch': 'away_emblem.png',
            'emblem_busy': 'busy_emblem.png',
            'emblem_phone': 'busy_emblem.png',
            'emblem_offline': 'offline_emblem.png',
            'emblem_hidden': 'offline_emblem.png',
            'emblem_blocked': 'blocked_emblem.png',
        }

class aMSNSmileyLoader(aMSNGenericLoader):
    def __init__(self):
        aMSNGenericLoader.__init__(self, "smileys")
        self._keys = {
            'smiley_airplane': 'airplane.png',
            'smiley_angel': 'angel.png',
            'smiley_angry': 'angry.png',
            'smiley_ball': 'ball.png',
            'smiley_bat': 'bat.png',
            'smiley_beer': 'beer.png',
            'smiley_big_smile': 'big_smile.png',
            'smiley_bowl': 'bowl.png',
            'smiley_boy': 'boy.png',
            'smiley_brb': 'brb.png',
            'smiley_broken_heart': 'broken_heart.png',
            'smiley_cake': 'cake.png',
            'smiley_camera': 'camera.png',
            'smiley_car': 'car.png',
            'smiley_cat': 'cat.png',
            'smiley_cigarette': 'cigarette.png',
            'smiley_clapping_hands': 'clapping_hands.png',
            'smiley_clock': 'clock.png',
            'smiley_coffee': 'coffee.png',
            'smiley_computer': 'computer.png',
            'smiley_confused': 'confused.png',
            'smiley_cool_glasses': 'cool_glasses.png',
            'smiley_crying': 'crying.png',
            'smiley_dead_rose': 'dead_rose.png',
            'smiley_devil': 'devil.png',
            'smiley_disapointed': 'disapointed.png',
            'smiley_dog': 'dog.png',
            'smiley_dont_know': 'dont_know.png',
            'smiley_drink': 'drink.png',
            'smiley_email': 'email.png',
            'smiley_embarrassed': 'embarrassed.png',
            'smiley_eye_rolling': 'eye_rolling.png',
            'smiley_film': 'film.png',
            'smiley_finger_cross': 'finger_cross.png',
            'smiley_gift': 'gift.png',
            'smiley_girl': 'girl.png',
            'smiley_goat': 'goat.png',
            'smiley_handcuffs': 'handcuffs.png',
            'smiley_heart': 'heart.png',
            'smiley_im': 'im.png',
            'smiley_island': 'island.png',
            'smiley_kiss': 'kiss.png',
            'smiley_left_hug': 'left_hug.png',
            'smiley_light': 'light.png',
            'smiley_mobile': 'mobile.png',
            'smiley_money': 'money.png',
            'smiley_moon': 'moon.png',
            'smiley_msn': 'msn.png',
            'smiley_nerd': 'nerd.png',
            'smiley_note': 'note.png',
            'smiley_party': 'party.png',
            'smiley_phone': 'phone.png',
            'smiley_pizza': 'pizza.png',
            'smiley_plate': 'plate.png',
            'smiley_quiet': 'quiet.png',
            'smiley_rabbit': 'rabbit.png',
            'smiley_rain': 'rain.png',
            'smiley_rainbow': 'rainbow.png',
            'smiley_right_hug': 'right_hug.png',
            'smiley_rose': 'rose.png',
            'smiley_sad': 'sad.png',
            'smiley_sarcastic': 'sarcastic.png',
            'smiley_secret': 'secret.png',
            'smiley_sheep': 'sheep.png',
            'smiley_shock': 'shock.png',
            'smiley_sick': 'sick.png',
            'smiley_smile': 'smile.png',
            'smiley_snail': 'snail.png',
            'smiley_star': 'star.png',
            'smiley_storm': 'storm.png',
            'smiley_sun': 'sun.png',
            'smiley_teeth': 'teeth.png',
            'smiley_think': 'think.png',
            'smiley_thumb_down': 'thumb_down.png',
            'smiley_thumb_up': 'thumb_up.png',
            'smiley_tired': 'tired.png',
            'smiley_tongue': 'tongue.png',
            'smiley_turtle': 'turtle.png',
            'smiley_umbrella': 'umbrella.png',
            'smiley_wink': 'wink.png',
            'smiley_xbox': 'xbox.png',
        }
