# -*- coding: utf-8 -*-

from collections import namedtuple
from support.common import plugin

import support.titleformat as tf

class Episode(namedtuple('Episode', ['series_id', 'series_code', 'season_number',
  'episode_number', 'title_en', 'title_ru', 'date', 'rating', 'watched', 'list_title'])):

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
          'premiered': self.episode_date,
          'episode': self.episode_number,
          'season': self.season_number,
          'plot': None,
          'rating': self.rating,
          'studio': None,
          'castandrole': [],
          'writer': None,
          'director': None,
          'genre': None,
          'tvshowtitle': self.list_title,
          'year': None,
      },
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
  def episode_url(self):
    return plugin.url_for('play_episode',
      series_id = self.series_id,
      season_number = self.season_number,
      episode_number = self.episode_number,
      select_quality = True
    )

  @property
  def episode_date(self):
    import datetime
    import time
    date = datetime.date(*(time.strptime(self.date, '%d.%m.%Y')[0:3]))
    return date.strftime('%Y-%m-%d')

    # str_to_date(release_date, '%d.%m.%Y %H:%M')
    # date_to_str(e.release_date, '%Y-%m-%d')

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
