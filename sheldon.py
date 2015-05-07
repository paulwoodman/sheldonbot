#! /usr/bin/env python
# this is a scaffold for a multi network irc bot using the twisted framework

import re
import sys
import unicodedata
import requests
import uktime
from bs4 import BeautifulSoup
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet import ssl
from twisted.python import log
from twisted.words.protocols import irc

################################################################################
########                        S e t t i n g s                         ########
################################################################################
identity = {
    'twistedbot': {
        'nickname': 'sheldonbot-',
        'realname': 'Sheldon IRC Bot',
        'username': 'Sheldonbot',
        'nickserv_pw': None
    },
}
networks = {
    'rackspace': {
        'host': 'irc.rackspace.com',
        'port': 6697,
        'ssl': True,
        'identity': identity['twistedbot'],
        'autojoin': (
            '#ukahlinux',
        )
    }
}
CHANNEL = '#ukahlinux'

################################################################################

class TwistedBot(irc.IRCClient):
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        print('sheldonbot signed on')

        network = self.factory.network

        if network['identity']['nickserv_pw']:
            self.msg('NickServ', 
                'IDENTIFY %s' % network['identity']['nickserv_pw'])

        for channel in network['autojoin']:
            print('join channel %s' % channel)
            self.join(channel)

    def joined(self, channel):
        print('joined channel')
    
    def privmsg(self, user, channel, msg):
       print('[%s] <%s> %s' % (channel, user, msg))

    def alterCollidedNick(self, nickname):
        return nickname+'_'

    def _get_nickname(self):
        return self.factory.network['identity']['nickname']
    def _get_realname(self):
        return self.factory.network['identity']['realname']
    def _get_username(self):
        return self.factory.network['identity']['username']
    nickname = property(_get_nickname)
    realname = property(_get_realname)
    username = property(_get_username)

    def privmsg(self, user, channel, msg):

        if 'bazinga' in msg.lower():
             dam = self._get_help()
	     self.msg(CHANNEL, dam)

        if 'help' in msg.lower():
             helpz = self._get_helpz()
             self.msg(CHANNEL, helpz)

        if 'uktime' in msg.lower():
             timez = self._get_time()
             self.msg(CHANNEL, timez)


    def _get_help(self):
	return (" The roommate agreement is here: http://10.190.239.14")
    
    def _get_helpz(self):
	return ("Do you really need Sheldon's help???")

    def _get_time(self):
        return uktime.localtime


class TwistedBotFactory(protocol.ClientFactory):
    protocol = TwistedBot

    def __init__(self, network_name, network):
        self.network_name = network_name
        self.network = network

    def clientConnectionLost(self, connector, reason):
        print('client connection lost')
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print('client connection failed')
        reactor.stop()

if __name__ == '__main__':
    for name in networks.keys():
        factory = TwistedBotFactory(name, networks[name])
        
        host = networks[name]['host']
        port = networks[name]['port']

        if networks[name]['ssl']:
            reactor.connectSSL(host, port, factory, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(host, port, factory)

    reactor.run()


