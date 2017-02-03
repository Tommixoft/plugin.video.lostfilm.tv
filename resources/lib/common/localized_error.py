# -*- coding: utf-8 -*-

# from common.plugin import plugin
from support.common import plugin
from vendor.causedexception import CausedException

class LocalizedError(CausedException):
  def __init__(self, lang_code, reason, *args, **kwargs):
    CausedException.__init__(self, **kwargs)
    self.reason = reason
    self.reason_args = args
    self.lang_code = lang_code

  @property
  def localized(self):
    return plugin.get_string(self.lang_code) % self.reason_args

  def __str__(self):
    if isinstance(self.reason, basestring):
      return self.reason % self.reason_args
    else:
      return str(self.reason)
