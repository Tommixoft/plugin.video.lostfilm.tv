# -*- coding: utf-8 -*-

from common.plugin import plugin
from lostfilm.series import Series

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
  from common.services import xrequests_session
  from lostfilm.dom_parser import DomParser
  return DomParser()
