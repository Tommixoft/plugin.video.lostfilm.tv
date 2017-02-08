# -*- coding: utf-8 -*-
import logging
import re
import json

from lostfilm.menuentry import MenuEntry
import support.titleformat as tf

class LFmenu(object):

    def menu(self):
        menu_items = []   
        
        # ======= CREATE MENU ITEMS ============ #
        menu_fav = ['My Favorites','Избранные сериалы','favorites']
        menu_favnews = ['New episodes of favorites','Избранные сериалы Hовинки','favnews']

        # ======= ADD MENU ITEMS ============ #
        menu_items.append(MenuEntry(*menu_fav).list_item())
        menu_items.append(MenuEntry(*menu_favnews).list_item())

        return menu_items 

