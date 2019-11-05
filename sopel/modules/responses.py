"""This module sends responses to frequently posted messages at #miraheze."""

from sopel.module import commands import example

@commands('request')
@example('.request')
def addchan(bot, trigger):
    """Reply to channel request message."""
    bot.say(("Pining RhinosF1 and Examknow to let them know of your request")),
            '#XtremeBNC')
    if trigger.sender != '#ZppixBot':
        bot.reply("Request sent! Action upon the request should be taken shortly. Thank you for using Xtreme")


@commands('gj', 'gw')
@example('.gj (nick)')
def gj(bot, trigger):
    """Tell the user that they are doing good work."""
    bot.say(("You're doing good work, {}!").format(trigger.group(2)))
