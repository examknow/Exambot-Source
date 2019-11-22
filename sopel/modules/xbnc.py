from sopel import module

@module.rule('!request', '!admin', '!help')
def hi(bot, trigger):
   bot.reply('Welcome ' + trigger.nick + ' an administrator will be with you shortly. Thank you for choosing XtremeBNC.')
   bot.reply('Please note that if you are outside of operating hours, we may not see your request until later. Please bear with us')
   bot.say('Examknow, RhinosF1: ' + trigger.nick + ' has requested an administrator on ' + trigger.sender + ' please take action', '#XtremeBNC-staff')
