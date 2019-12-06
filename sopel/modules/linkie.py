from sopel import module

@module.rule('\[\[.*\]\]')
def Oper_link (bot, trigger):
    bot.say('https://simple.wikipedia.org/wiki/' + trigger.group(2))
