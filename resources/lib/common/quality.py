# -*- coding: utf-8 -*-

from common.attribute import Attribute

class Quality(Attribute):
  def get_lang_base(self):
      return 40208

  SD = (0, 'sd')
  HD_720 = (1, 'mp4', 'hd', 'MP4')
  HD_1080 = (2, '1080p', '1080')

  def __lt__(self, other):
      return self.id < other.id
