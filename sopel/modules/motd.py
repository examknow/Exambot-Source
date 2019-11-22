################################################################
#                Created 11.22.19 by Examknow                  #
#                UserFile Module for ExamBot                   #
#                ANY REMOVAL OR MODIFICATION                   #
#       OF THIS HEADER IS A VIOLATION OF THE COPYING LICENCE   #
################################################################
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

import os
import re
import codecs
from sopel.module import rule, commands, example, event

DEFAULT_CHANNEL = '#ExamBot'
USERNAME_RE = re.compile(r'[A-Za-z0-9\[\]\{\}\-_|`]+$')
CHANNEL_RE = re.compile(r'#[A-Za-z0-9#\-]+$')

#get the location of the userfile
def get_filename(bot):
    name = 'userfile.db'
    return os.path.join(bot.config.core.homedir, name)


def setup(bot):
    bot.userfilename = get_filename(bot)
    bot.userfile = load_userfile(bot.userfilename)

#Load the list of users from the userfile
def load_userfile(filename):
    known_users = {}
    if os.path.isfile(filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        for line in f:
            line = line.rstrip('\n')
            if '\t' in line:
                channel, username = line.split('\t')
            else:
                channel = DEFAULT_CHANNEL
                username = line

            if channel in known_users:
                known_users[channel].append(username)
            else:
                known_users[channel] = [username]
    return known_users

#write the userfile
def write_userfile(filename, userfilename):
    f = codecs.open(filename, 'w', encoding='utf-8')
    for channel in userfile:
        for user in userfile[channel]:
            f.write('{}\t{}\n'.format(channel, user))
    f.close()


@event('JOIN')
@rule('.*')
def send_motd(bot, trigger):
#if the bot triggers the MOTD then ignore
    if trigger.nick == bot.nick:
        return
#if user is not in the channel's userfile then send the MOTD
    if trigger.sender not in bot.userfile:
        bot.userfile[trigger.sender] = []

    if trigger.nick not in bot.userfile[trigger.sender]:
        if trigger.sender == '#XtremeBNC':
            message = ("Hi. Welcome to XtremeBNC.")
	if trigger.sender == '#ExamBot':
	    message = ("Welcome to my channel")
        else:
            return

        bot.say('MOTD from ' + trigger.sender + ': ' + message, trigger.nick)
        bot.userfile[trigger.sender].append(trigger.nick)
        write_userfile(get_filename(bot), bot.userfile)


# initialize the bot's global adminfile


DEFAULT_CHANNEL = '#ExamBot'
USERNAME_RE = re.compile(r'[A-Za-z0-9\[\]\{\}\-_|`]+$')
CHANNEL_RE = re.compile(r'#[A-Za-z0-9#\-]+$')


def get_filename(bot):
    name = 'adminfile.db'
    return os.path.join(bot.config.core.homedir, name)


def setup(bot):
    bot.adminfilename = get_filename(bot)
    bot.adminfile = load_adminfile(bot.adminfilename)


def load_adminfile(filename):
    known_admins = {}
    if os.path.isfile(filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        for line in f:
            line = line.rstrip('\n')
            username = line
            known_admins = [username]
    return known_admins

#write the userfile
def write_userfile(filename, adminfilename):
    f = codecs.open(filename, 'w', encoding='utf-8')
    f.write('{}\n'.format(user))
    f.close()

#set up admin commands
@commands('addchanuser')
@example('.addchanuser <nick> <channel>')
def add_known_user(bot, trigger):
    """Add user to known users list."""
    if trigger.nick not in bot.config.core.admins:
        bot.reply('Only bot admins set the userfile')
        return

    username = trigger.group(3)
    if trigger.group(4):
        channel = trigger.group(4)
    elif trigger.sender[0] == '#':
        channel = trigger.sender
    else:
        channel = DEFAULT_CHANNEL

    if not USERNAME_RE.match(username):
        bot.reply('Invalid username: {}'.format(username))
        return

    if not CHANNEL_RE.match(channel):
        bot.reply('Invalid channel name: {}'.format(channel))
        return

    if channel not in bot.known_users_list:
        bot.known_users_list[channel] = []

    if username in bot.known_users_list[channel]:
        bot.say('{} is already added to the userfile of channel {}'.format(
                username, channel
                ))
        return

    bot.known_users_list[channel].append(username)
    save_known_users_list(get_filename(bot), bot.known_users_list)
    bot.say('Okay, {} is now added to known users list of channel {}'.format(
            username, channel
            ))
