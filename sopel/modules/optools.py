# coding=utf-8
#################################################################
# Created 11.11.2019                                            #
# Based off channelmgmt.py from ZppixBot by Zppix (Pix1234)     #
# Authored by Examknow for the ExamBot IRC bot                  #
# (https://github.com/examknow/Exambot-Source)                  #
# Any removal or modification of this header is a violation     #
# of the copyright licence                                      #
#################################################################
from __future__ import unicode_literals, absolute_import, print_function, division

import re
import time

from sopel import formatting
from sopel.module import (
    commands, example, priority, OP, require_chanmsg
)
from sopel.tools import Identifier


def default_mask(trigger):
    welcome = formatting.color('Welcome to:', formatting.colors.PURPLE)
    chan = formatting.color(trigger.sender, formatting.colors.TEAL)
    topic_ = formatting.bold('Topic:')
    topic_ = formatting.color('| ' + topic_, formatting.colors.PURPLE)
    arg = formatting.color('{}', formatting.colors.GREEN)
    return '{} {} {} {}'.format(welcome, chan, topic_, arg)


def get_chanops(bot, trigger):
    chanops = 'Examknow'
    if str(trigger.sender) == '##RhinosF1':
        chanops = ['RhinosF1']
    elif str(trigger.sender) == '##Examknow':
	chanops = ['Examknow']
    elif str(trigger.sender) == '#ExamBot':
        chanops = ['Examknow']
    elif str(trigger.sender) == '#XtremeBNC':
	chanops = ['Examknow', 'RhinosF1']
    elif str(trigger.sender) == '#XtremeBNC-staff':
	chanops = ['Examknow', 'RhinosF1']
    elif str(trigger.sender) == '#XtremeBNC-feed':
	chanops = ['Examknow', 'RhinosF1']
    else:
        bot.say('Please ask a bot admininstrator to set up channel management for this channel', trigger.sender)
    return chanops


@require_chanmsg
@commands('op')
def op(bot, trigger):
    """
    Command to op users in a room. If no nick is given, Sopel will op the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "+o", nick])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('deop')
def deop(bot, trigger):
    """
    Command to deop users in a room. If no nick is given, Sopel will deop the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "-o", nick])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('voice')
def voice(bot, trigger):
    """
    Command to voice users in a room. If no nick is given, Sopel will voice the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "+v", nick])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('devoice')
def devoice(bot, trigger):
    """
    Command to devoice users in a room. If no nick is given, the nick who sent the command will be devoiced
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "-v", nick])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('kick')
@priority('high')
def kick(bot, trigger):
    """Kick a user from the channel."""
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    nick = opt
    channel = trigger.sender
    reasonidx = 2
    if not opt.is_nick():
        if argc < 3:
            return
        nick = text[2]
        channel = opt
        reasonidx = 3
    reason = ' '.join(text[reasonidx:])
    if nick != bot.config.core.nick and trigger.nick in chanops:
        bot.write(['KICK', channel, nick, ':' + reason])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


def configureHostMask(mask):
    if mask == '*!*@*':
        return mask
    if re.match('^[^.@!/]+$', mask) is not None:
        return '%s!*@*' % mask
    if re.match('^[^@!]+$', mask) is not None:
        return '*!*@%s' % mask

    m = re.match('^([^!@]+)@$', mask)
    if m is not None:
        return '*!%s@*' % m.group(1)

    m = re.match('^([^!@]+)@([^@!]+)$', mask)
    if m is not None:
        return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match('^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None:
        return '%s!%s@*' % (m.group(1), m.group(2))
    return ''


@require_chanmsg
@commands('ban')
@priority('high')
def ban(bot, trigger):
    chanops = get_chanops(bot, trigger)
    """Ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    banmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+b', banmask])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('unban')
def unban(bot, trigger):
    """Unban a user from the channel. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    banmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '-b', banmask])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('quiet')
def quiet(bot, trigger):
    """Quiet a user. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    quietmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+q', quietmask])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('unquiet')
def unquiet(bot, trigger):
    """Unquiet a user. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    quietmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '-q', quietmask])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('kickban', 'kb')
@example('.kickban [#chan] user1 user!*@* get out of here')
@priority('high')
def kickban(bot, trigger):
    """Kick and ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 3:
        return
    opt = Identifier(text[1])
    nick = opt
    mask = text[2] if any([s in text[2] for s in "!@*"]) else ''
    channel = trigger.sender
    reasonidx = 3 if mask != '' else 2
    if not opt.is_nick():
        if argc < 5:
            return
        channel = opt
        nick = text[2]
        mask = text[3] if any([s in text[3] for s in "!@*"]) else ''
        reasonidx = 4 if mask != '' else 3
    reason = ' '.join(text[reasonidx:])
    mask = configureHostMask(mask)
    if mask == '':
        mask = nick + '!*@*'
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+b', mask])
        bot.write(['KICK', channel, nick, ':' + reason])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('topic')
def topic(bot, trigger):
    """Change the channel topic. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    if not trigger.group(2):
        return
    channel = trigger.sender.lower()

    narg = 1
    mask = None
    mask = bot.db.get_channel_value(channel, 'topic_mask')
    mask = mask or default_mask(trigger)
    mask = mask.replace('%s', '{}')
    narg = len(re.findall('{}', mask))

    top = trigger.group(2)
    args = []
    if top:
        args = top.split('~', narg)

    if len(args) != narg:
        message = "Not enough arguments. You gave {}, it requires {}.".format(
            len(args), narg)
        return bot.say(message)
    topic = mask.format(*args)
    if trigger.nick in chanops:
        bot.write(('TOPIC', channel + ' :' + topic))
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('tmask')
def set_mask(bot, trigger):
    """Set the topic mask to use for the current channel. Within the topic mask, {} is used to allow substituting in chunks of text. This mask is used when running the 'topic' command.
    """
    chanops = get_chanops(bot, trigger)
    if trigger.nick in chanops:
        bot.db.set_channel_value(trigger.sender, 'topic_mask', trigger.group(2))
        bot.say("Gotcha, " + trigger.nick)
    else:
        bot.reply('Log in as a Channel Operator to change this setting')


@require_chanmsg
@commands('showmask')
def show_mask(bot, trigger):
    """Show the topic mask for the current channel."""
    chanops = get_chanops(bot, trigger)
    if trigger.nick in chanops:
        mask = bot.db.get_channel_value(trigger.sender, 'topic_mask')
        mask = mask or default_mask(trigger)
        bot.say(mask)
    else:
        bot.reply('Log in as a Channel Operator to change this setting')
        
        
@require_chanmsg
@commands('invite')
def invite_user(bot, trigger):
    """
    Command to invite users to a room.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('doing...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
        nick = trigger.group(2)
        channel = trigger.sender
    if not nick:
        bot.say(trigger.nick + ": No user specified.", trigger.sender)
    elif trigger.nick in chanops:
        bot.write(['INVITE', channel, nick])
    else:
        bot.reply('Log in as a Channel Operator to change this setting')
