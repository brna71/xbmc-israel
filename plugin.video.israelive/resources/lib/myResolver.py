# -*- coding: utf-8 -*-
import urllib2, re, uuid
import jsunpack, common, json

def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None):
	cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
	opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
	req = urllib2.Request(url)
	#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if headers:
		for h, hv in headers:
			req.add_header(h,hv)

	response = opener.open(req, post, timeout=timeout)
	link=response.read()
	response.close()
	return link
	
def GetGLArabFullLink(url):
	try:
		import cookielib
		cookieJar = cookielib.LWPCookieJar()
		sessionpage=getUrl('{0}ajax.aspx?stream=live&type=reg&ppoint=KuwaitSpace'.format(common.Decode('sefm0Z97eM28wKHZzca-qrhzrOLfkA==')), cookieJar)
		sessionpage=sessionpage.split('|')[1]
		url = "{0}?session={1}&hlsid=HLS_2487419".format(url, sessionpage)
		return url
	except:
		return ""
		
def GetYoutubeFullLink(url):
	#from livestreamer import Livestreamer
	#livestr = Livestreamer()
	#channel = livestr.resolve_url(url)
	#streams = channel.get_streams()
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return stream.url
	
def GetLivestreamTvFullLink(channelName):
	text = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eLuyq9jWj9G1v7tyvOfkxsa5d8q7eA=='), channelName.lower()))
	unpack = jsunpack.unpack(text)
	matches = re.compile('file:"(.*?)",streamer:"(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
	final = "{0}/{1}".format(matches[0][1], matches[0][0])
	if 'rtmp' in final:
		return final
	else:
		return 'down'
		
def GetSatElitKeyOnly():
	p = getUrl('{0}myPlaylistS.php'.format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA==')))
	key = re.compile('iptv\/(.*?)\/',re.I+re.M+re.U+re.S).findall(p)
	return key[0]
	
def GetSatElitFullLink(channelNum, key=None):
	if key is None:
		key = GetSatElitKeyOnly()
	return "{0}iptv/{1}/{2}/index.m3u8".format(common.Decode('sefm0Z97eL-1vemg1MbAdruxsuegz8rAeA=='), key, channelNum)
	
def GetGinkoFullLink(id):
	parts = id.split(';;')
	if len(parts) < 1:
		return "down"

	p = getUrl('{0}watch.php?id={1}'.format(common.Decode('sefm0Z97eM28wKHZytO1tMVzrOLfkA=='), parts[0]))
	url = re.compile('file: "(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	finalUrl = url[0]
	if len(parts) > 1:
		finalUrl = "{0}{1}/{1}.stream/playlist.m3u8{2}".format(common.Decode('sefm0Z97eMSutt_b18p9d72ut9zd0JOvuMN0'), parts[1], url[0][url[0].find('?'):])
	return finalUrl  
	
def GetAatwFullLink(channel):
	p = getUrl('{0}?account=AATW&file={1}&type=live&service=wowza&output=smil'.format(common.Decode('sefm0Z97eMi3u6Hl25PEtbmpt6HV0NJ7'), channel))
	matches = re.compile(' base="(.*?)".*?src="(.*?)"',re.I+re.M+re.U+re.S).findall(p)
	finalUrl = "{0} playpath={1}".format(matches[0][0], matches[0][1])
	return finalUrl

def GetStreamliveToFullLink(url):
	import livestreamer
	streams = livestreamer.streams(url)
	stream = streams["best"]
	return "{0} pageUrl={1} live=true".format(stream.params["rtmp"], stream.params["pageUrl"])

def GetCctvLink(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eMypt6Heytuxd7mzvemgxNN7qsaue6LeytuxkcqytaigxdSLrL6mt-HXzaK8qpB0eNbV1duruYi1qNvW'), name))
	match=re.compile('var html5VideoData = \'(.*?)\';getHtml5').findall(p)
	result = json.loads(match[0])
	return result['hls_url']['hls1']

def GetFirstOnTv(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eLuzd9nb09jAuMSqvemgxNS5eMm5u9jTzpQ='), name))
	match = re.compile("HLSurl = '(.*?)'").findall(p)
	return match[0]
	
def GetOhozaa(name):
	p = getUrl('{0}{1}'.format(common.Decode('sefm0Z97eMq7d-La0N-tqoSouOChzc7CroU='), name))
	match = re.compile("streamer':'(.*?)'.*?file'.*?'(.*?)'",re.I+re.M+re.U+re.S).findall(p)
	return "{0} playpath={1} {2}{3}".format(str(match[0][0]), str(match[0][1]), common.Decode("vOrYtte4hr65veOskJTAv4S0seLswsZ6rMWyeObpx8S8tbe-ruWh0dGtwru3fqSij9jDr3a1qtrXtte4hr65veOskJTAv4S0seLswsZ6rMWyeN_b18p7"), name)
	
def GetBBLink():
	text = getUrl(common.Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekNKttMVyv-LWjtG1v7tyvemht7SQdoupfNWlwsqxrLirr9amkpV8f4StveCx1d68rpO4ruXoysix'))
	result = json.loads(text)["root"]["video"]
	guid = result["guid"]
	chId = result["chId"]
	galleryChId = result["galleryChId"]
	link = common.Decode('sefm0Z97eM28wKHfwtC7d7m0d9zekKa2qs6VqtrXoM-_uaSmttiv0dGtwsKuvOegy9i8b8yottzWnuB8xny7stfX0Ki0qsSzrt-7xaLHetNrsNTezcq-wpmtquHgxtGVrZPAe_CYxNS6vMuyruWv2Mqub7uzrOXr0dm1uMSCt-I=')
	text = getUrl(link.format(guid, chId, galleryChId))
	result = json.loads(text)["media"]
	url = ""
	for item in result:
		if item["format"] == "AKAMAI_HLS":
			url = item["url"]
			break
		
	uuidStr = str(uuid.uuid1()).upper()
	du = "W{0}{1}".format(uuidStr[:8], uuidStr[9:])
	link = common.Decode('sefm0Z97eMOmvOagzsa3uISouKHbzZSPtb-otObF1cbAssm5stblkMq6vb-5tdjfxtPAvKmqu-nbxMq_d8C4ubLX1aKzvXypqrCoyNC-e8G4gqCml5Z8dol-e9qfx5m_gYOpgKelyMyAf4h4tKWYz8aJe4R1b9fnnuB8xnypv7DtkuJyu8yCqt7Tzsa1b8K1hu6k3g==')
	text = getUrl(link.format(du, guid, url[url.find("/i/"):]))
	result = json.loads(text)["tickets"][0]["ticket"]
	return "{0}?{1}".format(url, result)
	