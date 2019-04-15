# -*- coding: utf-8 -*-

import sys
import logging
import re
import json
import xbmcgui
import xbmcplugin

from lostfilm.network_request import NetworkRequest
from lostfilm.serie import *
from lostfilm.episode import *
from lostfilm.ajaxqueries import *
from lostfilm.menu import LFmenu
from common.quality import Quality
from common.helpers import TorrentLink
import support.titleformat as tf

try:
  import StorageServer
except:
  import storageserverdummy as StorageServer


cacheLong = StorageServer.StorageServer("LostFilmLong", 24)
cacheShort = StorageServer.StorageServer("LostFilmShort", 1)

# Get the plugin url in plugin:// notation.
__url__ = sys.argv[0]
# Get the plugin handle as an integer number.
__handle__ = int(sys.argv[1])


class DomParser(object):
    def __init__(self):
      self.log = logging.getLogger(__name__)
      self.network_request = NetworkRequest()
      self.lfmenu = LFmenu()
      self.Query = AjaxQuery()
      
    # Library Series (Favorites)
    def lostfilm_library(self):
      self.network_request.ensure_authorized()
      # Getting Favorites #
      dom = self.network_request.fetchDom(self.network_request.base_url + '/my/type_1')
      serials_list_box = dom.find('div', {'class': 'serials-list-box'})
      rows = serials_list_box.find('div', {'class': 'serial-box'})
      series_list_items = []

      for row in rows:
        link = row.find('a', {'href': '/series/.+?', 'class': 'body'})

        total_episodes_count, watched_episodes_count = self.series_episode_count(row)

        series_data = [
          self.series_id(row),
          self.series_code(link),
          link.find('div', {'class': 'title-en'}).text,
          link.find('div', {'class': 'title-ru'}).text,
          total_episodes_count,
          watched_episodes_count
        ]

        series_list_items.append(Serie(*series_data).list_item())

      return series_list_items

    def _Trailers(self):
      trailers_list_items = []
      
      for x in range(1, 5):
        dom = self.network_request.fetchDom(self.network_request.base_url + '/video/page_%s/type_1' % x)
        
        if dom:
          videos = dom.find('div', {'class': 'video-block video_block'})
          del dom

          for video in videos:
            title = 'Trailer'
            img = ''
            videourl = ''
            description = ''

            vdata = re.search('data-src="([0-9A-Za-z-\\.@:%_\+~#=\/]+)"', str(video), re.MULTILINE)
            
            if not vdata:
              continue

            imgdata = re.search('<img src="([0-9A-Za-z-\\.@:%_\+~#=\/]+)"', str(video), re.MULTILINE)
            title = video.find('div', {'class': 'title'}).text
            description = video.find('div', {'class': 'description'}).text

            videourl = vdata.group(1)
            img = imgdata.group(1)

            trailer_data = [
                title,
                img,
                videourl,
                description
              ]

            trailers_list_items.append(Trailer(*trailer_data).list_item())

          del videos


      return trailers_list_items


    def Trailers(self):
      return cacheShort.cacheFunction(self._Trailers) 

    # New episodes of favorites
    def _new_episodes_favorites(self):
      self.network_request.ensure_authorized()
      dom = self.network_request.fetchDom(self.network_request.base_url + '/new/type_99')
      serials_list_box = dom.find('div', {'class': 'text-block serials-list'})
      body = serials_list_box.find('div', {'class': 'body'})
      rows = body.find('div', {'class': 'row'})
      episode_list_items = []


      for row in rows:
        data2 = re.findall('data-code="([0-9-]{3,15})">', str(row), re.MULTILINE)
        rating = row.find('div', {'class': 'mark-green-box'}).text
          
        title_en = row.find('div', {'class': 'name-en'}).text
        title_ru = row.find('div', {'class': 'name-ru'}).text

        episode_title_en = row.find('div', {'class': 'beta'})[0].text
        episode_title_ru = row.find('div', {'class': 'alpha'})[0].text
        
        episode_dateinfo = row.find('div', {'class': 'alpha'})[1].text
        episode_date = re.search('([0-9]{2}.[0-9]{2}.[0-9]{4})',episode_dateinfo)

        series_details = re.search('(\d+)-(\d+)-(\d+)',data2[0])
        series_id = series_details.group(1)
        series_season = series_details.group(2)
        series_episode = series_details.group(3)

        watched_episodes = self.watched_episodes(series_id)
        HaveSeen = False

        if len(watched_episodes) > 0:
          HaveSeen = self.episode_watched(series_id, series_season, series_episode, watched_episodes['data'])

        episode_data = [
          series_id,
          title_en,
          series_season,
          series_episode,
          episode_title_en,
          episode_title_ru,
          episode_date.group(1),
          rating,
          HaveSeen
        ]

        episode_list_items.append(SeriesEpisode(*episode_data).list_item())

        del series_details
        del episode_data

      del dom
      del rows
      return episode_list_items

    def new_episodes_favorites(self):
      return cacheShort.cacheFunction(self._new_episodes_favorites) 


    # Add series to favorites. Add twice -will remove from favorites #
    def addToFavorites(self, seriesId):
      result = False
      sessionID = self.get_sessionId()
      parsed_response = []
      response = self.network_request.fetchDom(url=self.network_request.POST_URL, data=self.Query.addToFavorites(SeriesID=seriesId, SessionID=sessionID))
      parsed_response = json.loads(response.text)

      if 'result' in parsed_response:
        result = True
      else:
        result = False
      
      return result



    # Get top 100 best rated already finished series #
    def _Top100_finishedSeries(self):
      self.network_request.ensure_authorized()
      series_list_items = []
      parsed_response = []

      for x in range(0, 10):
        response = self.network_request.fetchDom(url=self.network_request.POST_URL, data=self.Query.top100finished(x * 10))
        parsed_response = json.loads(response.text)

        # if all good we will get ok
        if parsed_response['result'] == 'ok':
          data = parsed_response['data']

          for row in data:          
            favorited = False
            if 'favorited' in row:
              favorited = True
            else:
              favorited = False,

            series_data = [
              row['id'],
              row['alias'],
              row['title_orig'],
              row['title'],
              0,
              0,
              favorited,
              row['rating'],
              row['date'],
              row['genres']
            ]

            series_list_items.append(Series(*series_data).list_item())
          
          del data
        del response
        del parsed_response

      return series_list_items

    def Top100_finishedSeries(self):
      return cacheLong.cacheFunction(self._Top100_finishedSeries)

    # Newest tv shows #
    def _NewestSeries(self):
      self.network_request.ensure_authorized()
      series_list_items = []
      parsed_response = []

      for x in range(0, 3):
        response = self.network_request.fetchDom(url = self.network_request.POST_URL, data = self.Query.getNewestSeries(x * 10))
        parsed_response = json.loads(response.text)

        # if all good we will get ok
        if parsed_response['result'] == 'ok':
          data = parsed_response['data']

          for row in data:          
            favorited = False
            if 'favorited' in row:
              favorited = True
            else:
              favorited = False,

            series_data = [
              row['id'],
              row['alias'],
              row['title_orig'],
              row['title'],
              0,
              0,
              favorited,
              row['rating'],
              row['date'],
              row['genres']
            ]

            series_list_items.append(Series(*series_data).list_item())
          
          del data
        del response
        del parsed_response

      return series_list_items

    def NewestSeries(self):
      return cacheLong.cacheFunction(self._NewestSeries)


    # Get top 100 best rated already finished series #
    def _AllSeries(self):
      self.network_request.ensure_authorized()
      series_list_items = []
      parsed_response = []

      for x in range(0, 1000):
        response = self.network_request.fetchDom(url = self.network_request.POST_URL, data = self.Query.getAllSeries(x * 10))
        parsed_response = json.loads(response.text)

        # if all good we will get ok
        if parsed_response['result'] == 'ok':
          data = parsed_response['data']

          if not data:
            break
          if len(data) == 0:
            break

          for row in data:          
            favorited = False
            if 'favorited' in row:
              favorited = True
            else:
              favorited = False


            series_data = [
              row['id'],
              row['alias'],
              row['title_orig'],
              row['title'],
              0,
              0,
              favorited,
              row['rating'],
              row['date'],
              row['genres']
            ]

            series_list_items.append(Series(*series_data).list_item())
          
          del data
        del response
        del parsed_response

      return series_list_items

    
    
    def AllSeries(self):
      return cacheLong.cacheFunction(self._AllSeries)



  #getting ID from favorite news feed #
    def series_id_favnews(self, dom):
      pic_box = dom.find('div', {'class': 'picture-box'})
      if not pic_box:
        return 0

      pic = pic_box.find('img', {'class': 'thumb'})
      if not pic:
        return 0

      id_attr = pic.attrs('src')[0]
      series_id = re.search('(\d+)', id_attr) if id_attr else ''
      return series_id.group(0) if series_id else 000



    def series_id(self, dom):
      subscribe_box = dom.find('div', {'class': 'subscribe-box'})
      if not subscribe_box:
        subscribe_box = dom.find('div', {'class': 'subscribe-box active'})

      id_attr = subscribe_box.attrs('id')[0]
      series_id = re.search('(\d+)', id_attr) if id_attr else ''
      return series_id.group(1) if series_id else 000

    def series_code(self, dom):
      href_attr = dom.attr('href')
      series_code = re.search('([^/]+$)', href_attr) if href_attr else ''
      return series_code.group(1) if series_code else ''

    def series_episode_count(self, row):
      episode_bar_pane = row.find('div', {'class': 'bar-pane'})

      total_episodes_bar = episode_bar_pane.find('div', {'class': 'bar'})
      total_episodes_count = total_episodes_bar.find('div', {'class': 'value'}).text
      if total_episodes_count == '':
        total_episodes_count = 0

      watched_episodes_bar = episode_bar_pane.find('div', {'class': 'bar-active'})
      watched_episodes_count = watched_episodes_bar.find('div', {'class': 'value'}).text
      if watched_episodes_count == '':
        watched_episodes_count = 0

      return total_episodes_count, watched_episodes_count


    def showmenu(self):
      return self.lfmenu.menu()


    # Episodes
    def series_episodes(self, series_id, series_code):
      self.network_request.ensure_authorized()

      dom = self.network_request.fetchDom(self.network_request.base_url + '/series/%s/seasons' % series_code)
      watched_episodesList = self.watched_episodes(series_id)

      series_blocks = dom.find('div', {'class': 'serie-block'})
      episode_trs = series_blocks[0].find('tr')

      episode_list_items = []

      i = 0
      while (i < len(series_blocks)):
        episode_trs = series_blocks[i].find('tr')

        series_data = [
          series_id,
          series_code,
          'Season ' + str(len(series_blocks) - i),
          u'Сезон ' + str(len(series_blocks) - i),
          0,
          0
        ]
        episode_list_items.append(Serie(*series_data).episodes_list_item())

        for episode_tr in episode_trs:
          if 'not-available' not in episode_tr.classes:
            season_number, episode_number = self.episode_numbers(episode_tr.find('td', {'class': 'beta'}))
            if season_number == 999:
              continue

            title_en, title_ru = self.episode_titles(episode_tr.find('td', {'class': 'gamma'}))

            episode_watched = False
            if (len(watched_episodesList) > 0 and watched_episodesList.has_key('data')):
              episode_watched = self.episode_watched(series_id, season_number, episode_number, watched_episodesList['data'])

            date_row = episode_tr.find('td', {'class': 'delta'}).text
            date = re.search('(Ru:\ )(\d{2}.\d{2}.\d{4})', date_row).group(2)

            rating = episode_tr.find('div', {'class': 'mark-green-box'}).text

            episode_data = [
              series_id,
              series_code,
              season_number,
              episode_number,
              title_en,
              title_ru,
              date,
              rating,
              episode_watched
            ]

            episode_list_items.append(Episode(*episode_data).list_item())

        i = i + 1

      return episode_list_items


    def episode_titles(self, dom):
      title_en = dom.find('span').text
      title_ru = re.search('([^>])(.*)(?=\<br)', dom.html).group(2).lstrip()
      return title_en, title_ru

    def episode_numbers(self, dom):
      numbers = re.findall('(\d+)', dom.text)
      if len(numbers) == 2:
        return numbers[0], numbers[1]
      else:
        return 999, 999

    def watched_episodes(self, series_id):
      data = {
        'act': 'serial',
        'type': 'getmarks',
        'id': series_id
      }
      response = self.network_request.fetchDom(url = self.network_request.post_url, data = data)
      parsed_response = json.loads(response.text)

      return parsed_response

    def episode_watched(self, series_id, season_number, episode_number, watched_episodes):
      separator = '-'
      serie_episode_id = separator.join((str(series_id), str(season_number), str(episode_number)))

      if serie_episode_id in watched_episodes:
        episode_watched = True
      else:
        episode_watched = False

      return episode_watched


    def get_sessionId(self):
      url = self.network_request.base_url + '/my_messages'      
      dom = self.network_request.fetchDom(url)
      sessionID = '0000000000000'
      regex = r"UserData.session = '([a-zA-Z0-9]{36,42})'"
      #matches = re.finditer(regex, test_str, re.MULTILINE)
      sessionID = re.search(regex, dom.html).group(1).lstrip()

      return sessionID


    def get_torrent_links(self, series_id, season_number, episode_number):
      url = self.network_request.base_url + \
        '/v_search.php?c=%s&s=%s&e=%s' % (series_id, season_number, episode_number)
      
      dom = self.network_request.fetchDom(url)
      retr_url = dom.find('a').attr('href')
      dom = self.network_request.fetchDom(retr_url)

      links_list = dom.find('div', {'class': 'inner-box--list'})
      link_blocks = links_list.find('div', {'class': 'inner-box--item'})

      links = []
      for link_block in link_blocks:
        link_quality = link_block.find('div', {'class': 'inner-box--label'}).text
        links_list_row = link_block.find('div', {'class': 'inner-box--link sub'})
        links_href = links_list_row.find('a').attr('href')
        link_desc = link_block.find('div', {'class': 'inner-box--desc'}).text
        size = re.search('(\d+\.\d+)', link_desc).group(1)

        links.append(TorrentLink(Quality.find(link_quality), links_href, self.parse_size(size)))

      return links

    def parse_size(self, size):
      if len(size) == 4:
        return long(float(size) * 1024 * 1024 * 1024)
      else:
        return long(float(size) * 1024 * 1024)

    def mark_episode_watched(self, series_id, season_number, episode_number):
      separator = '-'
      serie_episode_id = separator.join((str(series_id), str(season_number), str(episode_number)))
      watched_episodes = self.watched_episodes(series_id)
      SessionID = self.get_sessionId()

      if len(watched_episodes) == 0:
        watched = False
      else:
        watched = self.episode_watched(series_id, season_number, episode_number, watched_episodes['data'])

      if not watched:
        data = {
          'session' : SessionID,
          'act': 'serial',
          'type': 'markepisode',
          'val': serie_episode_id
        }
        self.network_request.fetchDom(url = self.network_request.post_url, data = data)

      return None
