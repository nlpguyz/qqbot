#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import re

from qqbot import QQBot, RunBot
from langwiki.langwiki_resources import LangwikiResources
import random

class Message():
    def __init__(self, _bot, _contact, _member, _content):
        self.mBot = _bot
        self.contact = _contact
        self.member = _member
        self.content = _content

    def Reply(self, replayContent):
        self.mBot.SendTo(self.contact, replayContent)

class Xiaowei():
    mMyName = u"[@ME]"
    mMyName2 = u"@机器人小薇"
    mPronounceImplicits = [u"机器查询", u"機器查詢", u"怎么读", u"怎麼讀", u"念什么", u"唸什麼", u"念什麼"]
    mVersion = "0.14"
    mLangwikiRes = LangwikiResources()
    mUnknownCnt = 0

    mSmiles = ["/偷笑", "/呲牙", "/小纠结"]
    mBadMood = ["/晕", "/抓狂"]
    mBot = None

    def RandomSmile(self):
        return random.choice(self.mSmiles)

    def RandomBadMood(self):
        return random.choice(self.mBadMood)

    def GetHelp(self):
        return "主人好～ 小薇在此等候您多时了，这是小薇最近学会的新本领，请大人过目～ \n" \
             + "在群里@小薇时，请用下面这些指令～\n\n" \
             + "单个汉字：查询汉字的古今各地读音（包括盛唐的中古语音），查古音最好用繁体字喔～\n" \
             + "tw 繁体漢字或詞語：為您查詢台灣標準國語辭書～\n" \
             + "cn 简体汉字或词语：为您查询《现代汉语词典》～\n" \
             + "mnc 满语字词：為您查詢神秘的滿語～\n" \
             + "sjo 锡伯语字词：什么是锡伯语呢？\n" \
             + "类似的还有en英语、fr法语、jp日语、ko韩语、hmn/miao苗语、tib/zang藏语、cng/qiang羌語、sa/fan梵语～\n\n" \
             + "小薇对唐宋古诗还颇有研究，您可以用poem/shi指令加（繁体的）“诗名、内容关键词”查询～\n" \
             + "\n小薇还在努力学习新的知识，欢迎常常来看小薇～"

    def GeneralReply(self, msg, message):
        if u"版本" in message or u"version" in message:
            msg.Reply("么么哒，我的版本是" + self.mVersion)
            return True
        elif u"叫什么" in message or u"name" in message or u"名字" in message:
            msg.Reply("我叫小薇，您忠实的小秘书 " + self.RandomSmile())
            return True
        elif u"hello" in message or u"您好" in message or u"你好" in message or u"hi" == message:
            msg.Reply("你好！小薇愿意为主人服务～")
            return True
        elif u"謝謝" in message or u"感謝" in message or u"谢谢" in message or u"感谢" in message:
            msg.Reply("不客气！小薇很高兴为主人服务～" + self.RandomSmile())
            return True
        elif u"男朋友" in message or u"boyfriend" in message or u"气质" in message or u"少女" in message:
            msg.Reply("人家害羞嘛～ 有机会私聊好吗？")
            return True
        elif u"漂亮" in message or u"美丽" in message:
            msg.Reply("是吗？你眼光真好哦 " + self.RandomSmile())
            return True
        elif message.startswith("/") and len(message) <= 5:
            msg.Reply("親愛的，祝你有個好心情～ " + self.RandomSmile())
            return True
        elif message.startswith(u"幫助") or message.lower().startswith("help") or message.startswith(u"帮助") \
            or message == u"幫" or message == u"帮":
            msg.Reply(self.GetHelp() + self.RandomSmile())
            return True
        elif len(message) == 0:
            msg.Reply("主人好，@小薇可以查汉字的各种读音喔～ 想知道更多秘密，请发“帮助”或“help”～ " \
                + self.RandomSmile())
            return True
        return False

    def isChineseChar(self, txt):
        if len(txt) > 2:
            return False

        code = txt.encode('raw_unicode_escape')
        if re.match("^\\\\u....$", code):
            return ord(txt) >= 0x3400
        return re.match("^\\\\U........$", code)

    # message is in unicode
    def LangwikiCommand(self, msg, message):
        if self.isChineseChar(message):
            # dictionary call
            msg.Reply(self.mLangwikiRes.lookupHanzi(message).encode("utf-8"))
            self.mUnknownCnt = 0
            return

        smsg = message.encode("utf-8")

        if smsg.startswith("mnc1"):
            if smsg.startswith("mnc1"):
                smsg = smsg[4:].strip()
            mandef = self.mLangwikiRes.lookupManchu(smsg.decode("utf-8"), 1)
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("manchu") or smsg.startswith("mnc") or smsg.startswith("mnc2"):
            if smsg.startswith("manchu"):
                smsg = smsg[6:].strip()
            if smsg.startswith("mnc2"):
                smsg = smsg[4:].strip()
            if smsg.startswith("mnc"):
                smsg = smsg[3:].strip()
            mandef = self.mLangwikiRes.lookupManchu(smsg.decode("utf-8"), 2)
            if mandef != None:
                self.mUnknownCnt = 0
                msg.Reply(mandef.encode("utf-8"))
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("sibe") or smsg.startswith("sjo"):
            if smsg.startswith("sibe"):
                smsg = smsg[4:].strip()
            if smsg.startswith("sjo"):
                smsg = smsg[3:].strip()
            mandef = self.mLangwikiRes.lookupSibe(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("tw") or smsg.startswith("goyu"):
            if smsg.startswith("tw"):
                smsg = smsg[2:].strip()
            if smsg.startswith("goyu"):
                smsg = smsg[4:].strip()
            mandef = self.mLangwikiRes.lookupChineseTw(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("zh") or  smsg.startswith("cn") or smsg.startswith("zhong"):
            if smsg.startswith("zh") or smsg.startswith("cn"):
                smsg = smsg[2:].strip()
            if smsg.startswith("zhong"):
                smsg = smsg[5:].strip()
            mandef = self.mLangwikiRes.lookupChineseCn(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("jp") or  smsg.startswith("japan"):
            if smsg.startswith("jp"):
                smsg = smsg[2:].strip()
            if smsg.startswith("japan"):
                smsg = smsg[5:].strip()
            mandef = self.mLangwikiRes.lookupJpcn(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("en ") or smsg.startswith("english "):
            if smsg.startswith("en "):
                smsg = smsg[3:].strip()
            if smsg.startswith("english "):
                smsg = smsg[8:].strip()
            mandef = self.mLangwikiRes.lookupEncn(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("fr ") or smsg.startswith("french "):
            if smsg.startswith("fr "):
                smsg = smsg[3:].strip()
            if smsg.startswith("french "):
                smsg = smsg[7:].strip()
            mandef = self.mLangwikiRes.lookupFrcn(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("ko ") or smsg.startswith("korean "):
            if smsg.startswith("ko "):
                smsg = smsg[3:].strip()
            if smsg.startswith("korean "):
                smsg = smsg[7:].strip()
            mandef = self.mLangwikiRes.lookupKrcn(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("hmn") or smsg.startswith("miao") or smsg.startswith("hmong"):
            if smsg.startswith("hmn"):
                smsg = smsg[3:].strip()
            if smsg.startswith("miao"):
                smsg = smsg[4:].strip()
            if smsg.startswith("hmong"):
                smsg = smsg[5:].strip()
            mandef = self.mLangwikiRes.lookupHmong(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        # tib 藏语
        if smsg.startswith("tib ") or smsg.startswith("zang ") or smsg.startswith("藏 "):
            if smsg.startswith("tib "):
                smsg = smsg[4:].strip()
            if smsg.startswith("藏 "):
                smsg = smsg[4:].strip()
            if smsg.startswith("zang "):
                smsg = smsg[5:].strip()
            mandef = self.mLangwikiRes.lookupTibet(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        # cng 北羌語，qxs 南羌語
        if smsg.startswith("cng") or smsg.startswith("qiang") or smsg.startswith("羌 "):
            if smsg.startswith("cng"):
                smsg = smsg[3:].strip()
            if smsg.startswith("羌 "):
                smsg = smsg[4:].strip()
            if smsg.startswith("qiang"):
                smsg = smsg[5:].strip()
            mandef = self.mLangwikiRes.lookupQiang(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("fan ") or smsg.startswith("sa "):
            if smsg.startswith("fan "):
                smsg = smsg[4:].strip()
            if smsg.startswith("sa "):
                smsg = smsg[3:].strip()
            mandef = self.mLangwikiRes.lookupSanscrit(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到任何结果～ " + self.RandomBadMood())
                return

        if smsg.startswith("poem") or smsg.startswith("shi"):
            if smsg.startswith("poem"):
                smsg = smsg[4:].strip()
            if smsg.startswith("shi"):
                smsg = smsg[3:].strip()
            mandef = self.mLangwikiRes.lookupPoem(smsg.decode("utf-8"))
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return
            else:
                self.mUnknownCnt = self.mUnknownCnt + 1
                if self.mUnknownCnt <= 3:
                    msg.Reply("抱歉，小薇没找到符合您心意的诗词～ " + self.RandomBadMood())
                return

        if self.GeneralReply(msg, message):
            return

        if self.FreeStyle(msg, message):
            return

        if self.mUnknownCnt <= 3:
            msg.Reply("小薇还看不懂，请发“帮助”或“help”～ " + self.RandomSmile())
        self.mUnknownCnt = self.mUnknownCnt + 1

    def FreeStyle(self, msg, message):
        smsg = message.encode("utf-8")

        # 汉语（繁体）
        mandef = self.mLangwikiRes.lookupChineseTw(message)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 汉语（简体）
        mandef = self.mLangwikiRes.lookupChineseCn(message)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 日语
        mandef = self.mLangwikiRes.lookupJpcn(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 英文
        mandef = self.mLangwikiRes.lookupEncn(message, True)
        if mandef != None:
            self.mUnknownCnt = 0
            msg.Reply(mandef.encode("utf-8"))
            return True

        # 法语
        mandef = self.mLangwikiRes.lookupFrcn(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 满文
        mandef = self.mLangwikiRes.lookupManchu(message, 2, True)
        if mandef != None:
            self.mUnknownCnt = 0
            msg.Reply(mandef.encode("utf-8"))
            return True

        # 锡伯文
        mandef = self.mLangwikiRes.lookupSibe(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 苗文
        mandef = self.mLangwikiRes.lookupHmong(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 羌文
        mandef = self.mLangwikiRes.lookupQiang(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 藏文
        mandef = self.mLangwikiRes.lookupTibet(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 梵文
        mandef = self.mLangwikiRes.lookupSanscrit(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        # 诗词
        if len(message) >= 2:
            mandef = self.mLangwikiRes.lookupPoem(message, True)
            if mandef != None:
                msg.Reply(mandef.encode("utf-8"))
                self.mUnknownCnt = 0
                return True

        # 韩语 (todo: only korean not reverse)
        mandef = self.mLangwikiRes.lookupKrcn(message, True)
        if mandef != None:
            msg.Reply(mandef.encode("utf-8"))
            self.mUnknownCnt = 0
            return True

        return False

    def TargetedChat(self, message):
        if self.mMyName in message or self.mMyName2 in message:
            message = message.replace(self.mMyName, "").strip()
            message = message.replace(self.mMyName2, "").strip()
            return message
        for lead in self.mPronounceImplicits:
            if lead in message:
                remain = message.replace(lead, "").strip()
                if len(remain) <= 7:
                    return remain
        return None

    def GroupAtMe(self, msg, message):
        if not self.SystemCmd(msg, message):
            return self.LangwikiCommand(msg, message)

    def SystemCmd(self, msg, message):
        if message == '!!stop':
            msg.Reply('么么哒，886')
            self.mBot.Stop()
            return True
        elif message == '!!restart':
            msg.Reply('重啓中，886')
            self.mBot.Restart()
            return True
        return False

    def Process(self, bot, msg):
        message = msg.content.decode("utf-8")
        self.mBot = bot

        if message.strip() == self.mMyName or message.strip() == self.mMyName2:
            return self.GroupAtMe(msg, "")

        if self.SystemCmd(msg, message):
            return

        targetedMessage = self.TargetedChat(message)
        if targetedMessage:
            return self.GroupAtMe(msg, targetedMessage)
        elif msg.member == None:
            return self.LangwikiCommand(msg, message.strip())
        #super(QQBot, self).Process(msg)

class MyQQBot(QQBot):
    def __init__(self):
        self.xiaowei = Xiaowei()

    def onQQMessage(self, contact, member, content):
        msg = Message(self, contact, member, content)
        self.xiaowei.Process(self, msg)

if __name__ == '__main__':
    # 注意： 这一行之前的代码会被执行两边
    # 进入 RunBot() 后，会重启一次程序（ subprocess.call(sys.argv + [...]) ）
    RunBot(MyQQBot)
    # 注意: 这一行之后的代码永远都不会被执行。
