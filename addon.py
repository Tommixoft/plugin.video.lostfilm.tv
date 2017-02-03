# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib', 'vendor'))

# from common.plugin import plugin
from support.common import plugin
from common.localized_error import LocalizedError

import lostfilm.routes

def launch():
  try:
    plugin.run()
  except LocalizedError as e:
    e.log()
    if e.kwargs.get('dialog'):
        xbmcgui.Dialog().ok(
          plugin.get_string(30000),
          *e.localized.split("|")
        )
    else:
        PluginHelper.notify(e.localized)
    if e.kwargs.get('check_settings'):
        plugin.open_settings()

if __name__ == '__main__':
  launch()
