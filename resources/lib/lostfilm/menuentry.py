# -*- coding: utf-8 -*-

from collections import namedtuple
from support.common import plugin
import support.titleformat as tf

class MenuEntry(namedtuple('MenuEntry', ['title_en', 'title_ru', 'path'])):
  def list_item(self):
    return {
      'label': self.title,
      'path': plugin.url_for(self.path),
      'is_playable': False,
      'thumbnail': None,
      'context_menu': self.context_menu
    }

  @property
  def context_menu(self):
    return [self.info_menu]

  @property
  def info_menu(self):
    # info_menu(s) + library_menu(s) + mark_series_watched_menu(s),
    return (plugin.get_string(40306), "Action(Info)")

  @property
  def series_url(self):
    return plugin.url_for('browse_series_episodes', series_id = self.id, series_code = self.code)

  @property
  def title(self):
    if plugin.get_setting('show-original-title', bool):
      return '%s' % (self.title_en)
    else:
      return '%s' % (self.title_ru)

