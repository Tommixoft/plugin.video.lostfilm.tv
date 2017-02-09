# -*- coding: utf-8 -*-
import logging
import re
import json

from support.common import plugin
from lostfilm.menuentry import MenuEntry
import support.titleformat as tf


class LFmenu(object):

    def menu(self):
        menu_items = []   
        
        # ======= CREATE MENU ITEMS ============ #
        menu_allseries = ['All Series','сериалы','allseries']
        menu_newestshows = ['Newest tv shows','новые Сериалы', 'newesttvshows']
        menu_fav = ['My Favorites','Избранные сериалы','favorites']        
        menu_favnews = ['New episodes of favorites','Избранные сериалы Hовинки', 'favnews']
        menu_bestfinished = ['100 Best rated finished tv shows','Топ 100 завершенных', 'bestfinished']

        # ======= ADD MENU ITEMS ============ #
        menu_items.append(MenuEntry(*menu_allseries).list_item())
        menu_items.append(MenuEntry(*menu_newestshows).list_item())
        menu_items.append(MenuEntry(*menu_fav).list_item())
        menu_items.append(MenuEntry(*menu_favnews).list_item())
        menu_items.append(MenuEntry(*menu_bestfinished).list_item())

        return menu_items 

