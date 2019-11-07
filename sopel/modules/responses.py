"""This module is based off of the responses module from ZppixBot (https://github.com/Pix1234/ZppixBot-Source)"""

from sopel.module import commands import example

@commands('request')
@example('.request <channel>')
def addchan(bot, trigger):
    """Reply to channel request message."""
    bot.say(("Examknow: " + trigger.nick + "has requested ExamBot on " + trigger.group(2) + " would you like me to join the channel?"  )),
            '#ExamBot')
    if trigger.sender != '#ExamBot':
        bot.reply("A requests has been sent to the administrators of the bot")


@commands('gj', 'gw')
@example('.gj (nick)')
def gj(bot, trigger):
    """Tell the user that they are doing good work."""
    bot.say(("You're doing good work, {}!").format(trigger.group(2)))
