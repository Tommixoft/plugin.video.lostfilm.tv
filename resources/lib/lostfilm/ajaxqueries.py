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

# Follow (add to favorites) tv show 
  def addToFavorites(self, SeriesID):
    return {
      'act': 'serial',
      'type': 'follow',
      'id': SeriesID
    }

# Get newest tv shows by most new 
  def getNewestSeries(self, showfrom):
    return {
      'act': 'serial',
      'type': 'search',
      'o': showfrom,
      's': '3',
      't': '1'
    }


  def getMyFavorites(self, showfrom):
    return {
      'act': 'serial',
      'type': 'search',
      'o': showfrom,
      's': '2',
      't': '99'
    }


  def getAllSeries(self, showfrom):
    return {
      'act': 'serial',
      'type': 'search',
      'o': showfrom,
      's': '2',
      't': '0'
    }    