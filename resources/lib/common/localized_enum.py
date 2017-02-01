# -*- coding: utf-8 -*-

from common.plugin import plugin
from vendor.enum import Enum
from vendor.ordereddict import OrderedDict

class LocalizedEnum(Enum):
  @property
  def lang_id(self):
    raise NotImplementedError()

  @property
  def localized(self):
    return plugin.get_string(self.lang_id)

  @classmethod
  def strings(cls):
    d = [(i.name, i.localized(plugin.get_string)) for i in cls]
    return OrderedDict(sorted(d, key=lambda t: t[1]))

  def __lt__(self, other):
    return self.localized < other.localized

  def __str__(self):
    return self.localized
