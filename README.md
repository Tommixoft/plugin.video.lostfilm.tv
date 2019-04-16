# plugin.video.lostfilm.tv
LostFilm.tv addon for Kodi. This plugin uses LostFilm API so your favorites will be sinchronized with LostFilm.TV, your watched episodes will be sinchronized with LostFilm.Tv
LostFilm loves to make changes to website that prevents this plugin from working correctly - when i find that plugin is broken i try to fix it.


This plugin offers such features:
* Ru, En language, Titles.
* All tv shows
* My Favorites 
* Newest Tv Shows
* New episodes of my favorites (10 so far. Not very usful so not high importance)
* Top rated 100 finished tv shows 
* Latest trailers

**Things that mostly will not be implemented:**
* Series plot (this requires many additional http requests and it's not optimal).
* Kodi library integration (i see no reason for this.)


If you found bug submit them to [Issues](https://github.com/Tommixoft/plugin.video.lostfilm.tv/issues)

To use this plugin - you must have account in [lostfilm.tv](http://lostfilm.tv). Plugin gets all data from website, including favorites and what episodes you already seen. There is no local library.

## Installation ##

### Upgrade from old (original) plugin version ###
You **HAVE to uninstall and then delete old plugin folder** from C:\Users\Your-USER\AppData\Roaming\Kodi\addons\plugin.video.lostfilm.tv in windows.
Same applies to other OS users.

### New installation ###
Make sure you have installed [SuperRepo](https://superrepo.org/get-started/) it will handle dependencies of this plugin.
Then go to [Releases](https://github.com/Tommixoft/plugin.video.lostfilm.tv/releases) and download latest version zip. And install as usual AddOn from zip file.

And ofcourse go to AddOn settings and fill your LostFilm.tv account login details and other settings.
#### If you will have problem failing script.module.torrent2http dependency - you can get this addon (zip) [from here](https://github.com/Tommixoft/script.module.torrent2http/releases/) ####

### Plugin no longer works?: ###
LostFilm.tv added capcha protection. You MUST go to their website and login manually, then your device will eb able to login withouth capcha. You have to do this from 1 IP. Because LostFilm.tv remembers capcha settings based on IP. This hack works 100%.






