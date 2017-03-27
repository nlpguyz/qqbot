#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
from qqbot import QQBot
from qqbot.qqbotcls import QQMessage
from qqbot.messagefactory import Message

class MyQQBot(QQBot):
    mMyName = u"@机器人小薇"
    mVersion = "0.02"

    def GeneralReply(self, msg):
        message = msg.content.decode("utf-8")
        if u"版本" in message or u"ver" in message:
            msg.Reply("么么哒，我的版本是" + self.mVersion)
            return True
        elif u"叫什么" in message or u"name" in message or u"名字" in message:
            msg.Reply("我叫小薇，您忠实的语言维基小秘书 [笑]")
            return True
        return False

    def GroupAtMe(self, msg):
        message = msg.content.decode("utf-8")
        message = message.replace(self.mMyName, "").strip()
        if len(message) == 1:
            # dictionary call
            msg.Reply(message.encode("utf-8") + ' 字典未上綫 抱歉 [囧]')
        elif not self.GeneralReply(msg):
            msg.Reply("小薇还看不懂，请以后再试 [笑]");

    def Process(self, msg):
        if (type(msg) is QQMessage):
            message = msg.content.decode("utf-8")
            if message == u'hi' or u"你好" in message or u"ohayo" in message:
                msg.Reply('么么哒，我是机器人小薇')
            elif self.mMyName in message:
                return self.GroupAtMe(msg)
            elif message == '!!stop':
                self.Stop(code=0)
                msg.Reply('么么哒，886')

        super(QQBot, self).Process(msg)

try:
  bot = MyQQBot()
  bot.LoginAndRun()
except KeyboardInterrupt:
  sys.exit(0)
