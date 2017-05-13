#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import random, time, sys, subprocess
import requests
import json
import html
import HTMLParser

class LangwikiResources:
    def __init__(self):
        return

    def lookupHanzi(self, hanzi):
        url = 'http://langwiki.org/tools/dict/php/query.php'
        #url = 'http://localhost/php/query.php'
        settings = [
            "0", # pu
            "4", # ct
            "0", # kr
            "0", # vn
            "0", # jp
            "0", # ltco
            "1", # ltcp
            "0", # match
            "0", # mn
            "0"  # wu
        ]

        # Set POST fields here
        post_fields = {
			"string": hanzi,
			"mode": "0",
			"flag[]": [
                "0", # only
                "0", # variants
                "1"  # annotation
            ],
			"setting[]": settings,
            "bot": "1"
        }

        r = requests.post(url, data = post_fields)
        if r.status_code != 200:
            return hanzi + u" 請讓小薇好好想想這個問題。。。（服务器快点啊）"

        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"太好了，主人，小薇給您找到了答案～ "
            answer += res["HTML"]
        else:
            answer = u"嗚嗚，這個字小薇暫時想不起來了～ 請稍後再問我吧"
        return answer

    def lookupManchuInv(self, han, ver):
        url = 'http://langwiki.org/tools/dict/manchu/query' + str(ver) + '.php?han=' + han
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupManchu(self, manchu, ver, freestyle = False):
        url = 'http://langwiki.org/tools/dict/manchu/query' + str(ver) + '.php?manchu=' + manchu
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"主人，原來這是滿語呢～\n" if freestyle else u"太好了，主人，小薇查到了～\n"
            answer += manchu + u"\n"
            answer += res["HTML"]
            return answer
        # Try chinese - manchu
        if ver == 2 and not freestyle:
            data = self.lookupManchuInv(manchu, ver)
            if data:
                answer = u"太好了，主人，小薇查到了解釋中含“" + manchu + u"”的滿語詞～\n"
                answer += data
                return answer
        return None

    def lookupSibeInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/manchu/querysibe.php?han=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupSibe(self, sibe, freestyle = False):
        url = 'http://langwiki.org/tools/dict/manchu/querysibe.php?sibe=' + sibe
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是锡伯语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupSibeInv(sibe)
            if data:
                answer = u"太好了，主人，小薇查到了解释中含“" + sibe + u"”的锡伯语词～\n"
                answer += data
                return answer
        else:
            return None

    def lookupChineseTw(self, queryString):
        url = 'http://langwiki.org/tools/dict/chinese/query.php?q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"主人，这个词小薇觉得是这个意思～ \n"
            answer += res["HTML"]
            return answer
        else:
            return None

    def lookupChineseCn(self, queryString):
        url = 'http://langwiki.org/tools/dict/chinese/query.php?t=cn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"主人，这个词小薇觉得是这个意思～ \n"
            answer += res["HTML"]
            return answer
        else:
            return None

    def lookupJpcn(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=jpcn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是日语呢～\n" if freestyle else u"主人，这个词小薇觉得是这个意思～ \n"
            answer += res["HTML"]
            return answer
        else:
            return None

    def lookupKrcn(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=krcn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是韩语呢～\n" if freestyle else u"太好了，主人，小薇查到了～ \n"
            answer += res["HTML"]
            return answer
        else:
            return None

    def lookupFrcnInv(self, han):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=frcn&h=' + han
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupFrcn(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=frcn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是法语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupFrcnInv(queryString)
            if data:
                answer = u"太好了，主人，小薇找到了～\n"
                answer += data
                return answer
        else:
            return None

    def lookupEncn(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=encn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是英语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += HTMLParser.HTMLParser().unescape(res["HTML"])
            return answer
        elif not freestyle:
            data = self.lookupEncnInv(queryString)
            if data:
                answer = u"太好了，主人，小薇找到了～\n"
                answer += data
                return answer
        else:
            return None

    def lookupEncnInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=encn&h=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = res["HTML"]
            return answer
        else:
            return None

    def lookupHmongInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/chinese/miao/query.php?h=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupHmong(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/chinese/miao/query.php?q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是苗语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupHmongInv(queryString)
            if data:
                answer = u"太好了，主人，小薇查到了解释中含“" + queryString + u"”的苗语词～\n"
                answer += data
                return answer
        return None

    def lookupSanscritInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=sacn&h=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupSanscrit(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/lang/query.php?lang=sacn&q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是梵语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupSanscritInv(queryString)
            if data:
                answer = u"太好了，主人，小薇查到了解释中含“" + queryString + u"”的梵语词～\n"
                answer += data
                return answer
        return None

    def lookupQiangInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/chinese/qiang/query.php?h=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupQiang(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/chinese/qiang/query.php?q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是羌语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupQiangInv(queryString)
            if data:
                answer = u"太好了，主人，小薇查到了解释中含“" + queryString + u"”的羌语词～\n"
                answer += data
                return answer
        return None

    def lookupTibetInv(self, queryString):
        url = 'http://langwiki.org/tools/dict/chinese/tibet/query.php?h=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            return res["HTML"]
        return None

    def lookupTibet(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/chinese/tibet/query.php?q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = u"原来是藏语呢～\n" if freestyle else u"太好了，主人，小薇找到了～\n"
            answer += res["HTML"]
            return answer
        elif not freestyle:
            data = self.lookupTibetInv(queryString)
            if data:
                answer = u"太好了，主人，小薇查到了解释中含“" + queryString + u"”的藏语词～\n"
                answer += data
                return answer
        return None

    def lookupPoem(self, queryString, freestyle = False):
        url = 'http://langwiki.org/tools/dict/poetry/query.php?q=' + queryString
        r = requests.get(url)
        if r.status_code != 200:
            return None
        res = json.loads(r.text)
        if "HTML" in res:
            answer = ""
            if res["type"] == "poem":
                answer = u"主人真有品味，这是您要找的诗词吗？\n\n" if freestyle else u"主人真有品味，小薇找到这首诗词了～\n\n"
                answer += res["HTML"]
            elif res["type"] == "list":
                if freestyle:
                    answer = u"主人是要找这些含有“" + queryString + u"”的古诗词吗？\n\n"
                else:
                    answer = u"小薇找到了这些含有“" + queryString + u"”的诗词，请您过目～\n\n"
                answer += res["HTML"]
                answer += u"\n\n因为诗词较多，请您告诉小薇更具体的篇名，或用“诗人:部分或完整篇名”的格式进行选择～"
            return answer
        else:
            return None
