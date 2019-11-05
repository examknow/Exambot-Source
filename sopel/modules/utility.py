_from sopel import module

@module.commands('request', 'requestchannel')
@module.example('.request <channel>')
def requestchannel(bot, trigger):
	if trigger.sender == '#ExamBot':
        	bot.say('Pinging Examknow to notify him of your request')

@module.commands('about')
def aboutbot(bot, trigger):
	bot.say('ExamBot Info: Version 3.0.0 | Operators are Examknow | For additional help you can go to exambot.miraheze.org/wiki/help | If the bot is acting up please report it by saying .report')

@module.commands('report')
def report(bot, trigger):
	bot.reply('sending incident report to ' + '#ExamBot')

