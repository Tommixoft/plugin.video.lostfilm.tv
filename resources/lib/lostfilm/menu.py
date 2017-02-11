# -*- coding: utf-8 -*-
from lostfilm.menuentry import MenuEntry


class LFmenu(object):

    def menu(self):
        menu_items = []

        # ======= CREATE MENU ITEMS ============ #
        menu_fav = ['  [B]My Favorites[/B] ››',
                    '  [B]Избранные сериалы[/B] ››',
                    'favorites'
                    ]

        menu_favnews = ['    New episodes of favorites ››',
                        '    Избранные сериалы Hовинки ››',
                        'favnews'
                        ]

        menu_allseries = ['  [B]All Series[/B] ››',
                          '  [B]сериалы[/B] ››',
                          'allseries'
                          ]

        menu_newestshows = ['  [B]Newest tv shows[/B] ››',
                            '  [B]новые Сериалы[/B] ››',
                            'newesttvshows'
                            ]

        menu_bestfinished = ['  [B]100 Best rated ended tv shows[/B] ››',
                             '  [B]Топ 100 завершенных[/B] ››',
                             'bestfinished'
                             ]

        menu_trailers = ['  [B]Latest Trailers[/B] ››',
                         '  [B]последний трейлеры[/B] ››',
                         'trailers'
                         ]

        # ======= ADD MENU ITEMS ============ #
        menu_items.append(MenuEntry(*menu_fav).list_item())
        menu_items.append(MenuEntry(*menu_favnews).list_item())

        menu_items.append(MenuEntry(*menu_allseries).list_item())
        menu_items.append(MenuEntry(*menu_newestshows).list_item())
        menu_items.append(MenuEntry(*menu_bestfinished).list_item())

        menu_items.append(MenuEntry(*menu_trailers).list_item())

        return menu_items
