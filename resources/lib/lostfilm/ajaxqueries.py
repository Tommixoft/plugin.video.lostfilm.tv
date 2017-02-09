# -*- coding: utf-8 -*-

from collections import namedtuple
from support.common import plugin

class AjaxQuery:

  def top100finished(self, showfrom):
    return {
      'act': 'serial',
      'type': 'search',
      'o': showfrom,
      's': '1',
      't': '5'
    } 