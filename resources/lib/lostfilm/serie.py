# -*- coding: utf-8 -*-

from collections import namedtuple
from support.common import plugin
import support.titleformat as tf

class Serie(namedtuple('Serie', ['id', 'code', 'title_en', 'title_ru', 'total_episodes', 'watched_episodes'])):
  def list_item(self):
    return {
      'label': self.title,
      'path': self.series_url,
      'is_playable': False,
      'thumbnail': self.poster,
      'properties': {
          'fanart_image': self.fanart_image,
      },
      'info': {
          'title': self.title,
          'episode': None,
          'original_title': self.title_en,
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
      'context_menu': self.context_menu
    }

  def episodes_list_item(self):
    return {
      'label': self.title,
      'path': self.series_url,
      'is_playable': False,
      'properties': {
          'fanart_image': self.fanart_image,
      }
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
  def poster(self):
    return 'http://static.lostfilm.tv/Images/%s/Posters/shmoster_s1.jpg' % self.id

  @property
  def fanart_image(self):
    return 'http://static.lostfilm.tv/Images/%s/Posters/poster.jpg' % self.id

  @property
  def title(self):
    if plugin.get_setting('show-original-title', bool):
      return '%s %s' % (self.title_en, self.unwatched_episode_count)
    else:
      return '%s %s' % (self.title_ru, self.unwatched_episode_count)

  @property
  def unwatched_episode_count(self):
    if int(self.total_episodes) == int(self.watched_episodes):
      return ''

    if int(self.total_episodes) == 0:
      return ''

    return ' (%s)' % tf.color(int(self.total_episodes) - int(self.watched_episodes), 'lime')
