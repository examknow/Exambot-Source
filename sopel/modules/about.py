#################################################################
# Created 11.6.2019                                             #
# Authored by Examknow for the ExamBot IRC bot                  #
# (https://github.com/examknow/Exambot-Source)                  #
# Any removal or modification of this header is a violation     #
# of the copyright licence                                      #
#################################################################
from sopel import module

@module.commands('about')
@module.example('.about')
@module.example('.about help')
def about(bot, trigger):
    argument = trigger.group(2)
    if argument == help
      bot.say("Examknow: I just recived a help request from " + trigger.nick + " in " + trigger.sender)
      bot.say("Help can be by saying .help in any ExamBot channel or ask an admin in #ExamBot")
    else
      bot.say("I am running ExamBot version 3.0.1 . If I am acting unstable please alert Examknow, my operator. For help say .about help. For a link to my source code on GitHub say .source . Thank you for choosing ExamBot.")

@module.commands('source', 'repo')
def source(bot, trigger):
  bot.say("My source code is avalible at https://github.com/Exambot-Source")
