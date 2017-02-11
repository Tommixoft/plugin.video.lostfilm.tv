# -*- coding: utf-8 -*-

import os
import pickle
import logging
import json
import hashlib

from requests import RequestException, Timeout
# from common.plugin import plugin
from support.common import plugin
from support.services import xrequests_session
from common.localized_error import LocalizedError
from support.abstract.proxylist import ProxyListException
from support.xrequests import NoValidProxiesFound, Session
from vendor.htmldocument import HtmlDocument
from vendor.timer import Timer

class NetworkRequest(object):
  USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
  BASE_URL = "https://www.lostfilm.tv"
  POST_URL = "https://www.lostfilm.tv/ajaxik.php"
  # BLOCKED_MESSAGE = "Контент недоступен на территории Российской Федерации"

  def __init__(self):
    self.log = logging.getLogger(__name__)
    self.cookie_jar = plugin.addon_data_path('cookies')
    self.session = xrequests_session()
    self.session.headers['User-Agent'] = self.USER_AGENT
    self.session.headers['Origin'] = self.BASE_URL
    self.cookie_str = None
    self.load_cookies()

  @property
  def base_url(self):
    return self.BASE_URL

  @property
  def post_url(self):
    return self.POST_URL

  @property
  def login(self):
    return plugin.get_setting('login', unicode)

  @property
  def password(self):
    return plugin.get_setting('password', unicode)

  def load_cookies(self):
    if self.cookie_jar and os.path.exists(self.cookie_jar):
      with open(self.cookie_jar, 'rb') as f:
        self.session.cookies = pickle.load(f)
        self.cookie_str = str(self.session.cookies)

  def save_cookies(self):
    if self.cookie_jar:
      new_cookie_str = str(self.session.cookies)
      if self.cookie_str != new_cookie_str:
        with open(self.cookie_jar, 'wb') as f:
          pickle.dump(self.session.cookies, f)
        self.cookie_str = new_cookie_str

  def fetch(self, url, params=None, data=None, **request_params):
      try:
        with Timer(logger=self.log, name='Fetching URL %s with params %r' % (url, params)):
          response = self.session.request('post' if data else 'get',
                                          url, params=params, data=data,
                                          **request_params)
          response.raise_for_status()
          if data:
            self.save_cookies()
          return response
      except Timeout as e:
        raise LocalizedError(32000, "Timeout while fetching URL: %s (%%s)" % url, plugin.get_string(30000), cause=e)
      except NoValidProxiesFound as e:
        raise LocalizedError(32005, "Can't find anonymous proxy", cause=e)
      except RequestException as e:
        raise LocalizedError(32001, "Can't fetch URL: %s (%%s)" % url, plugin.get_string(30000), cause=e)
      except ProxyListException as e:
        plugin.set_setting('use-proxy', 0)
        raise LocalizedError(32004, "Can't load anonymous proxy list", cause=e)

  def fetchDom(self, url, params=None, data=None, **request_params):
      response = self.fetch(url, params, data, **request_params)
      encoding = response.encoding
      if encoding == 'ISO-8859-1':
          encoding = 'utf-8'
      return HtmlDocument.from_string(response.content, encoding)

  def ensure_authorized(self):
    if not self.session.cookies.get('lf_session'):
      self.authorize()

  def authorize(self):
    with Timer(logger=self.log, name='Authorization'):
      try:
          self.session.cookies.clear('.lostfilm.tv')
      except KeyError:
          pass

      response = self.fetchDom(url = self.POST_URL, data = self.login_data)
      parsed_response = json.loads(response.text)

      if 'error' in parsed_response and parsed_response['error'] == 2:
        raise ScraperError(32003, "Authorization failed", check_settings=True)

  @property
  def login_data(self):
    return {
      'act': 'users', 'type': 'login', 'rem': '1',
      'mail': self.login, 'pass': self.password
    }
