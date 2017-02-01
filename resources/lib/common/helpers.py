# -*- coding: utf-8 -*-

from common.plugin import plugin

def notify(message, delay=10000):
    plugin.notify(
      message,
      plugin.get_string(30000),
      delay,
      plugin.addon.getAddonInfo('icon')
    )
