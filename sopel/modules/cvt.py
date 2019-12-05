################################################################
#                Created 12.3.19 by Examknow                   #
#     Miraheze Countervandalism Team Module for ExamBot        #
#                ANY REMOVAL OR MODIFICATION                   #
#       OF THIS HEADER IS A VIOLATION OF THE COPYING LICENCE   #
################################################################

from mwclient import Site
import logging
import mwclient
import json
logging.basicConfig(level=logging.WARNING)
with open('/mnt/nfs/labstore-secondary-tools-project/exambot/exambot/sopel/modules/config/trusted.json') as trusted_list:
    list = json.load(trusted_list)
with open('/mnt/nfs/labstore-secondary-tools-project/exambot/exambot/sopel/modules/config/config.json') as config_file:
    config = json.load(config_file)

stewards = list['stewards']
cvt = list['cvt']
sysadmins = list['sysadmins']
username = config['username']
password = config['password']
wikis = config['wikis']
ua = 'ExamBot 3.0 (examknow@xtremebnc.ml)'

def noaccount(bot, trigger):
	bot.say(trigger.hostmask + ' is not identified with services. This incident will be reported', trigger.sender)
	bot.say('Security Alert: ' + trigger.hostmask + ' on' + trigger.sender + ' attempted to use CVT without identifying with serivces.', '#ExamBot-logs')

import sopel
from sopel import module

@module.commands('block')
@module.example('.block meta Examknow 3 days')
def localblock(bot, trigger, username, password, Site):
	if trigger.account in stewards or trigger.account in cvt:
		options = trigger.group(2).split(" ")
		if len(options) == 2:
			wiki = options[0]
			target = options[1]
			site = Site(wiki + '.miraheze.org', clients_useragent=ua)
			site.login(username, password)
			api(query, http_method='POST', format='json', meta='tokens')
			for token in result['query']['tokens'].values():
				tokens = token['csrftoken']
				site.api(block, http_method='POST', format='json', user=target, expiry='3 days', nocreate=1, autoblock=1, token=tokens)
		elif len(options) > 2 and len(options) < 5:
			wiki = options[0]
			target = options[1]
			time = options[2]
			site = Site(wiki + '.miraheze.org', clients_useragent=ua)
			site.login(username, password)
			api(query, http_method='POST', format='json', meta='tokens')
			for token in result['query']['tokens'].values():
				tokens = token['csrftoken']
				site.api(block, http_method='POST', format='json', user=target, expiry=time, nocreate=1, autoblock=1, token=tokens)
		else:
			bot.reply('Syntax is .block <wiki> <target> <time>', trigger.sender)
		
		
	else:
		if trigger.account == '':
			noaccount()
		else:
			bot.say('Access Denied: ' + trigger.account + ' (' + trigger.hostmask + ') is not in the trusted list. This incident will be reported.', trigger.sender)
			bot.say('Security Alert: ' + trigger.account + ' (' + trigger.hostmask + ') attempted to use CVT on ' + trigger.sender, '#ExamBot-logs')
