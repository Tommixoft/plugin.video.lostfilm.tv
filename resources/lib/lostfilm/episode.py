# -*- coding: utf-8 -*-

from collections import namedtuple
# from common.plugin import plugin
from support.common import plugin

import support.titleformat as tf

class Episode(namedtuple('Episode', ['series_id', 'series_code', 'season_number',
  'episode_number', 'title_en', 'title_ru', 'watched'])):

  def list_item(self):
    return {
      'label': self.list_title,
      'path': self.episode_url,
      'is_playable': True,
      'thumbnail': self.poster,
      'icon': None,
      'properties': {
          'fanart_image': self.fanart_image,
      },
      'info': {
          'title': self.title,
          'originaltitle': self.title_en,
          'date': None,
          'plot': None,
          'rating': None,
          'studio': None,
          'castandrole': [],
          'writer': None,
          'director': None,
          'genre': None,
          'tvshowtitle': None,
          'year': None,
      },
      # 'context_menu': self.context_menu
    }

  @property
  def context_menu(self):
    return [self.info_menu]

  @property
  def info_menu(self):
    # info_menu(s) + library_menu(s) + mark_series_watched_menu(s),
    return (plugin.get_string(40306), "Action(Info)")

  # def series_url(self):
  #   return plugin.url_for('browse_series_episodes', series_code = self.code)
  @property
  def episode_url(self):
    return plugin.url_for('play_episode',
      series_id = self.series_id,
      season_number = self.season_number,
      episode_number = self.episode_number,
      select_quality = True
    )

  @property
  def poster(self):
    return 'http://static.lostfilm.tv/Images/%s/Posters/shmoster_s%s.jpg' \
      % (self.series_id, self.season_number)

  @property
  def fanart_image(self):
    return 'http://static.lostfilm.tv/Images/%s/Posters/poster.jpg' \
      % self.series_id

  @property
  def list_title(self):
    if self.watched:
      return self.title
    else:
      return tf.color(self.title, 'lime')

  @property
  def title(self):
    if plugin.get_setting('show-original-title', bool):
      return self.episode_number + '  -  ' + self.title_en
    else:
      return self.episode_number + '  -  ' + self.title_ru
