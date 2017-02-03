# -*- coding: utf-8 -*-

from xbmcswift2 import xbmcgui, xbmcvfs

import logging
import support.services as services
import support.titleformat as tf

from collections import namedtuple
from support.common import plugin
from common.quality import Quality
from support.common import save_files, purge_temp_dir

def notify(message, delay=10000):
    plugin.notify(message,
                  plugin.get_string(30000),
                  delay,
                  plugin.addon.getAddonInfo('icon'))

def singleton(func):
  memoized = []

  def singleton_wrapper(*args, **kwargs):
    if args or kwargs:
      raise TypeError("Singleton-wrapped functions shouldn't take any argument! (%s)" % func)

    memoized.append(func()) if not memoized else None
    return memoized[0]

  return singleton_wrapper

@singleton
def get_dom_parser():
  from support.services import xrequests_session
  from lostfilm.dom_parser import DomParser
  return DomParser()

def select_torrent_link(series_id, season_number, episode_number, select_quality = False):
  dom_parser = get_dom_parser()
  links = dom_parser.get_torrent_links(series_id, season_number, episode_number)

  qualities = sorted(Quality)
  quality = plugin.get_setting('quality', int)

  ordered_links = [next((l for l in links if l.quality == q), None) for q in qualities]

  if not quality or select_quality or not ordered_links[quality - 1]:
    filtered_links = [l for l in ordered_links if l]
    if not filtered_links:
      return
    options = ["%s / %s" % (tf.color(l.quality.localized, 'white'), tf.human_size(l.size)) for l in filtered_links]
    res = xbmcgui.Dialog().select(plugin.get_string(40400), options)
    if res < 0:
      return
    return filtered_links[res]
  else:
    return ordered_links[quality - 1]

def get_torrent(url):
  torrent = services.torrent(url)
  torrents_path = plugin.addon_data_path("torrents")
  xbmcvfs.mkdirs(torrents_path)
  torrent.download_locally(torrents_path)
  return torrent

def play_torrent(torrent, file_id=None):
  stream = services.torrent_stream()
  player = services.player()
  temp_files = stream.play(player, torrent, file_id=file_id)
  if temp_files:
    save_files(temp_files, rename=not stream.saved_files_needed, on_finish=purge_temp_dir)
  else:
    purge_temp_dir()

TorrentLink = namedtuple('TorrentLink', ['quality', 'url', 'size'])
