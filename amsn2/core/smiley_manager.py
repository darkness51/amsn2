# -*- coding: utf-8 -*-
#
# amsn - a python client for the WLM Network
#
# Copyright (C) 2010 Mehdi KOUHEN <arantes555@hotmail.fr>
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


class aMSNSmileyManager:
    def __init__(self, core): #for now, only a dic of default smileys' shortcuts
        self._core = core
        self.default_smileys_shortcuts = {
            "(ap)": "smiley_airplane",
            "(a)": "smiley_angel",
            ":-@": "smiley_angry",
            ":@": "smiley_angry",
            "(so)": "smiley_ball",
            ":-[": "smiley_bat",
            ":[": "smiley_bat",
            "(b)": "smiley_beer",
            ":D": "smiley_big_smile",
            ":>": "smiley_big_smile",
            ":->": "smiley_big_smile",
            ":-D": "smiley_big_smile",
            "(||)": "smiley_bowl",
            "(z)": "smiley_boy",
            "(brb)": "smiley_brb",
            "(u)": "smiley_broken_heart",
            "(^)": "smiley_cake",
            "(p)": "smiley_camera",
            "(au)": "smiley_car",
            "(@)": "smiley_cat",
            "(ci)": "smiley_cigarette",
            "(h5)": "smiley_clapping_hands",
            "(o)": "smiley_clock",
            "(c)": "smiley_coffee",
            "(co)": "smiley_computer",
            ":-s": "smiley_confused",
            ":s": "smiley_confused",
            "(h)": "smiley_cool_glasses",
            ":'(": "smiley_crying",
            "(w)": "smiley_dead_rose",
            "(6)": "smiley_devil",
            ":|": "smiley_disapointed",
            ":-|": "smiley_disapointed",
            "(&)": "smiley_dog",
            ":^)": "smiley_dont_know",
            "(d)": "smiley_drink",
            "(e)": "smiley_email",
            ":$": "smiley_embarrassed",
            ":-$": "smiley_embarrassed",
            "8-)": "smiley_eye_rolling",
            "(~)": "smiley_film",
            "(yn)": "smiley_finger_cross",
            "(g)": "smiley_gift",
            "(x)": "smiley_girl",
            "(nah)": "smiley_goat",
            "(%)": "smiley_handcuffs",
            "(l)": "smiley_heart",
            "*red+u": "smiley_im",
            "(ip)": "smiley_island",
            "(k)": "smiley_kiss",
            "({)": "smiley_left_hug",
            "(i)": "smiley_light",
            "(mp)": "smiley_mobile",
            "(mo)": "smiley_money",
            "(s)": "smiley_moon",
            "(m)": "smiley_msn",
            "8-|": "smiley_nerd",
            "(8)": "smiley_note",
            "<:o)": "smiley_party",
            "(t)": "smiley_phone",
            "(pi)": "smiley_pizza",
            "(pl)": "smiley_plate",
            ":-#": "smiley_quiet",
            "('.')": "smiley_rabbit",
            "(st)": "smiley_rain",
            "(r)": "smiley_rainbow",
            "(})": "smiley_right_hug",
            "(f)": "smiley_rose",
            ":(": "smiley_sad",
            ":-(": "smiley_sad",
            ":-<": "smiley_sad",
            ":<": "smiley_sad",
            "^o)": "smiley_sarcastic",
            ":-*": "smiley_secret",
            "(nah)": "smiley_sheep",
            ":-o": "smiley_shock",
            ":o": "smiley_shock",
            "+o(": "smiley_sick",
            ":)": "smiley_smile",
            ":-)": "smiley_smile",
            "(sn)": "smiley_snail",
            "(*)": "smiley_star",
            "(li)": "smiley_storm",
            "(#)": "smiley_sun",
            "8o|": "smiley_teeth",
            "*-)": "smiley_think",
            "(n)": "smiley_thumb_down",
            "(y)": "smiley_thumb_up",
            "|-)": "smiley_tired",
            ":p": "smiley_tongue",
            ":-p": "smiley_tongue",
            "(tu)": "smiley_turtle",
            "(um)": "smiley_umbrella",
            ";)": "smiley_wink",
            ";-)": "smiley_wink",
            "(xx)": "smiley_xbox",
        }
