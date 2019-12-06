from sopel import module

@module.commands('en', 'enwiki')
def enwiki(bot, trigger):
        bot.reply('http://en.wikipedia.org/wiki/' + trigger.group(2))

@module.commands('simple', 'simplewiki')
def simplewiki(bot, trigger):
        bot.reply('http://simple.wikipedia.org/wiki/' + trigger.group(2))

@module.commands('es', 'eswiki')
def eswiki(bot, trigger):
        bot.reply('http://es.wikipedia.org/wiki/' + trigger.group(2))

@module.commands('meta', 'metawiki', 'wmmeta')
def metawiki(bot, trigger):
        bot.reply('http://meta.wikimedia.org/wiki/' + trigger.group(2))

@module.commands('mw', 'mwwiki')
def mwwiki(bot, trigger):
        bot.reply('http://mediawiki.org/wiki/' + trigger.group(2))

@module.commands('mhmeta', 'mirahezemeta', 'mhmetawiki')
def mhmetawiki(bot, trigger):
        bot.reply('http://meta.miraheze.org/wiki/' + trigger.group(2))

@module.commands('ca', 'centralauth', 'wmca')
def wmca(bot, trigger):
        bot.reply('http://meta.wikimedia.org/wiki/Special:CentralAuth/' + trigger.group(2))

@module.commands('mhca')
def mhca(bot, trigger):
        bot.reply('http://meta.miraheze.org/wiki/Special:CentralAuth/' + trigger.group(2))

@module.commands('mhphab')
def mhphab(bot, trigger):
        bot.reply('http://phabricator.miraheze.org/' + trigger.group(2))

@module.commands('mhphab')
def wmphab(bot, trigger):
        bot.reply('http://phabricator.wikimedia.org/' + trigger.group(2)

@module.commands('mh')
@module.example('.mh <wiki name> <page name>')
def mhwiki(bot, trigger):
    try:
        options = trigger.group(2).split(" ")
        if len(options) == 1:
            page = options[0]
            bot.say("https://meta.miraheze.org/wiki/" + page)
        elif len(options) == 2:
            wiki = options[0]
            page = options[1]
            bot.say("https://" + wiki + ".miraheze.org/wiki/" + page)
    except AttributeError:
        bot.say('Syntax is .mh wiki page', trigger.sender)
