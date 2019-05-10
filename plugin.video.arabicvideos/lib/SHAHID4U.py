# -*- coding: utf-8 -*-
from LIBRARY import *

website0a = 'https://on.shahid4u.net'
script_name='SHAHID4U'
headers = { 'User-Agent' : '' }
menu_name='[COLOR FFC89008]SHA [/COLOR]'

def MAIN(mode,url,text):
	if mode==110: MENU()
	elif mode==111: ITEMS(url)
	elif mode==112: PLAY(url)
	elif mode==113: EPISODES(url)
	elif mode==119: SEARCH(text)
	return

def MENU():
	addDir(menu_name+'بحث في الموقع','',119)
	#addDir(menu_name+'المضاف حديثا',website0a,111)
	html = openURL(website0a,'',headers,'','SHAHID4U-MENU-1st')
	html_blocks = re.findall('navigation-menu(.*?)</div>',html,re.DOTALL)
	#xbmcgui.Dialog().ok(html,html)
	block = html_blocks[0]
	items = re.findall('href="http(.*?)">(.*?)<',block,re.DOTALL)
	ignoreLIST = ['مسلسلات انمي','الرئيسية']
	#keepLIST = ['مسلسلات ','افلام ','برامج','عروض','كليبات','اغانى']
	for link,title in items:
		title = title.strip(' ')
		if not any(value in title for value in ignoreLIST):
		#	if any(value in title for value in keepLIST):
			addDir(menu_name+title,'http'+link,111)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def ITEMS(url):
	#xbmcgui.Dialog().ok(url,url)
	html = openURL(url,'',headers,'','SHAHID4U-ITEMS-1st')
	html_blocks = re.findall('page-content(.*?)tags-cloud',html,re.DOTALL)
	block = html_blocks[0]
	items = re.findall('src="(.*?)".*?href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
	allTitles = []
	itemLIST = ['فيلم','اغنية','كليب','اعلان','هداف','مباراة','عرض','مهرجان','البوم']
	for img,link,title in items:
		link = unquote(link)
		title = title.strip(' ')
		title = unescapeHTML(title)
		if 'مشاهدة' in title or '/film/' in link or any(value in title for value in itemLIST):
			addLink(menu_name+title,link,112,img)
		elif 'الحلقة' in title and '/episode/' in link:
			episode = re.findall('(.*?) الحلقة [0-9]+',title,re.DOTALL)
			if episode:
				title = episode[0]
				if title not in allTitles:
					addDir(menu_name+title,link,113,img)
					allTitles.append(title)
		else:
			addDir(menu_name+title,link,113,img)
	html_blocks = re.findall('class="pagination(.*?)</div>',html,re.DOTALL)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('<a href=["\'](http.*?)["\'].*?>(.*?)<',block,re.DOTALL)
		for link,title in items:
			link = unescapeHTML(link)
			title = unescapeHTML(title)
			title = title.replace('الصفحة ','')
			if title!='':
				addDir(menu_name+'صفحة '+title,link,111)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def EPISODES(url):
	if '/series/' in url:
		url2 = url+'/episodes'
		html = openURL(url2,'',headers,'','SHAHID4U-ITEMS-1st')
		html_blocks = re.findall('container page-content(.*?)pagination',html,re.DOTALL)
	else:
		html = openURL(url,'',headers,'','SHAHID4U-ITEMS-1st')
		html_blocks = re.findall('ti-list-numbered(.*?)</div>',html,re.DOTALL)
	if not html_blocks or '/post/' in url:
		title = re.findall('details col-12 col-m-9.*?<h1>(.*?)</h1>',html,re.DOTALL)
		addLink(title[0],url,112)
	if html_blocks:
		block = html_blocks[0]
		items = re.findall('href="(.*?)".*?<h3>(.*?)<',block,re.DOTALL)
		itemsNEW = []
		for link,title in items:
			sequence = re.findall('الحلقة-([0-9]+)',link.split('/')[-1],re.DOTALL)
			if sequence: itemsNEW.append([link,int(sequence[0])])
			#xbmcgui.Dialog().ok(link.split('/')[-1],sequence[0])
		#name = xbmc.getInfoLabel('ListItem.Label')
		if itemsNEW:
			items = sorted(itemsNEW, reverse=True, key=lambda key: key[1])
		else:
			items = sorted(items, reverse=True, key=lambda key: key[0])
		for link,title in items:
			title = link.split('/')[-1].replace('-',' ')
			addLink(title,link,112)
	xbmcplugin.endOfDirectory(addon_handle)
	return

def PLAY(url):
	import xbmcaddon
	settings = xbmcaddon.Addon(id=addon_id)
	previous_url = settings.getSetting('previous.url')
	if url==previous_url:
		linkLIST = settings.getSetting('previous.linkLIST')
		linkLIST = linkLIST[1:-1].replace('&apos;','').replace(' ','').replace("'",'')
		linkLIST = linkLIST.split(',')
		#xbmcgui.Dialog().ok(url,str(linkLIST))
	else:
		headers = { 'User-Agent':'' }
		linkLIST = []
		#urlLIST = []
		parts=url.split('/')
		# watch links
		url2 = url.replace(parts[3],'watch')
		html = openURL(url2,'',headers,'','SHAHID4U-PLAY-1st')
		html_blocks = re.findall('class="servers-list(.*?)</div>',html,re.DOTALL)
		if html_blocks:
			block = html_blocks[0]
			items = re.findall('data-embedd="(.*?)".*?server_image">\n(.*?)\n',block,re.DOTALL)
			if items:
				id = re.findall('post_id=(.*?)"',html,re.DOTALL)
				if id:
					id2=id[0]
					for link,title in items:
						link = website0a+'/?postid='+id2+'&serverid='+link+'&name='+title
						linkLIST.append(link)
			else:
				items = re.findall('data-embedd="(.*?)"',block,re.DOTALL)
				for link in items:
					linkLIST.append(link)
		# download links
		url2 = url.replace(parts[3],'download')
		html = openURL(url2,'',headers,'','SHAHID4U-PLAY-2nd')
		id = re.findall('postId:"(.*?)"',html,re.DOTALL)
		if id:
			id2=id[0]
			headers = { 'User-Agent':'' , 'X-Requested-With':'XMLHttpRequest' }
			url2='https://shahid4u.net/ajaxCenter?_action=getdownloadlinks&postId='+id2
			html = openURL(url2,'',headers,'','SHAHID4U-PLAY-3rd')
			items = re.findall('href="(.*?)"',html,re.DOTALL)
			for link in items:
				linkLIST.append(link)
		#url2 = url + '?watch=1'
		#html = openURL(url2,'',headers,'','SHAHID4U-PLAY-2nd')
		#xbmcgui.Dialog().ok(html,html)
		#html_blocks = re.findall('li.server"(.*?)id="DataServers',html,re.DOTALL)
		#block = html_blocks[0]
		#items = re.findall('url: \'(.*?)\'.*?data: \'(.*?)\'',block,re.DOTALL)
		#url2 = items[0][0]+'?'+items[0][1]
		#items = re.findall('server\((.*?)\)',block,re.DOTALL)
		#for server in items:
		#	#html = openURL(url2+server,'',headers,'','SHAHID4U-PLAY-3rd')
		#	urlLIST.append(url2+server)
		#count = len(urlLIST)
		#import concurrent.futures
		#with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
		#	responcesDICT = dict( (executor.submit(openURL, urlLIST[i], '', #headers,'','SHAHID4U-PLAY-3rd'), i) for i in range(0,count) )
		#for response in concurrent.futures.as_completed(responcesDICT):
		#	html = response.result()
		#	#html = html.replace('SRC=','src=')
		#	links = re.findall('src="(.*?)"',html,re.DOTALL)
		#	linkLIST.append(links[0])
		settings.setSetting('previous.url',url)
		settings.setSetting('previous.linkLIST',str(linkLIST))
	from RESOLVERS import PLAY as RESOLVERS_PLAY
	#xbmcgui.Dialog().ok('',str(len(linkLIST)))
	#xbmcgui.Dialog().ok(url,str(linkLIST[8:20]))
	RESOLVERS_PLAY(linkLIST,script_name)
	return

def SEARCH(search=''):
	if search=='': search = KEYBOARD()
	if search == '': return
	search = search.replace(' ','+')
	url = website0a + '/search?s=' + search
	#xbmcgui.Dialog().ok(url,url)
	ITEMS(url)
	return



