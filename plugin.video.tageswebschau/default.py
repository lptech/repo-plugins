#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

pluginhandle = int(sys.argv[1])


def index():
    content = getUrl("http://www.radiobremen.de/extranet/tws/json/tws_toc.json?_=1367168129910")
    spl = content.split('{\n  	"titel" : ')
    for i in range(1, len(spl), 1):
        entry = spl[i]
        match = re.compile('"(.+?)"', re.DOTALL).findall(entry)
        title = match[0]
        title = cleanTitle(title)
        match = re.compile('"img" : "(.+?)"', re.DOTALL).findall(entry)
        thumb = match[0]
        title = cleanTitle(title)
        match = re.compile('"jsonurl" : "(.+?)"', re.DOTALL).findall(entry)
        url = "http://www.radiobremen.de"+match[0]
        addLink(title, url, 'playVideo', thumb)
    xbmcplugin.endOfDirectory(pluginhandle)


def playVideo(url):
    content = getUrl(url)
    match1 = re.compile('"url" : "http://(.+?)_L.mp4"', re.DOTALL).findall(content)
    match2 = re.compile('"url":"http://(.+?)_L.mp4"', re.DOTALL).findall(content)
    if match1:
        url = "http://"+match1[0]+"_L.mp4"
    elif match2:
        url = "http://"+match2[0]+"_L.mp4"
    listitem = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


def cleanTitle(title):
    return title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#039;", "\\").replace("&quot;", "\"").strip()


def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict


def addLink(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))

if mode == 'playVideo':
    playVideo(url)
else:
    index()
