#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
reload(sys)
from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator

sys.setdefaultencoding('utf8')
headers = requests.utils.default_headers()
headers.update(
{
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
)

fg = FeedGenerator()
fg.title(unicode("卡提諾正妹抱報"))
fg.link( href='https://ck101.com/forum.php?mod=forumdisplay&fid=1345&filter=typeid&typeid=3393', rel='alternate' )
fg.subtitle(unicode('自動產生正妹圖RSS'))
fg.load_extension('podcast')
fg.podcast.itunes_category('Fashion & Beauty', 'Podcasting')

#Fetch the issue list
r = requests.get('https://ck101.com/forum.php?mod=forumdisplay&fid=1345&filter=typeid&typeid=3393', headers=headers)
if r.status_code == requests.codes.ok:
    soup = BeautifulSoup(r.text, 'html.parser')
    issuelist = soup.find_all("a", string=re.compile(unicode("^卡提諾正妹抱報 [0-9]*期")))
    for issueidx, issuelink in enumerate(issuelist):
        #print(link.get('href'))
        #print(issuelink.text + ' ' +  issuelink.get('href'))
        #print "issueidx=" + str(issueidx)

        if issueidx>2:
            break

        #fetch the thread list
        r = requests.get(issuelink.get('href'), headers=headers)
        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            threadlist = soup.find(itemprop="articleBody").find_all("a", href=re.compile("^https:\/\/ck101\.com\/thread-[0-9-]*\.html"))
            for threadidx, threadlink in enumerate(threadlist):
                #print(threadlink.get('href'))
                #print "threadidx=" + str(threadidx)

                r = requests.get(threadlink.get('href'), headers=headers)
                if r.status_code == requests.codes.ok:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    title = soup.find("meta",  property="og:title")["content"]
                    #print title
                    description = soup.find("meta",  property="og:description")["content"]
                    #print description
                    imglist = soup.find(itemprop="articleBody").find_all("img", file!='')
                    for imgidx, imglink in enumerate(imglist):
                        #print imglink.get('file')
                        #print "imgidx=" + str(imgidx)
                        fe = fg.add_entry()
                        fe.id(imglink.get('file').replace("?_w=750",""))
                        fe.title(issuelink.text + " " + title)
                        fe.description(description)
                        #fe.enclosure(imglink.get('file'), 0)

    fg.rss_str(pretty=True)
    fg.rss_file('hottie_image.xml')
