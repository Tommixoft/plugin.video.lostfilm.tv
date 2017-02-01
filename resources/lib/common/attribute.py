# -*- coding: utf-8 -*-

from common.localized_enum import LocalizedEnum

class Attribute(LocalizedEnum):
  def get_lang_base(self):
    raise NotImplementedError()

  @property
  def lang_id(self):
    return self.get_lang_base() + self.id

  @property
  def id(self):
    return self.value[0]

  @property
  def filter_val(self):
    return self.value[1]

  def __repr__(self):
    return "<%s.%s>" % (self.__class__.__name__, self._name_)

  @classmethod
  def find(cls, what):
    for i in cls.__iter__():
      if what in i.value or i.name == what:
        return i
    return None
