#!/usr/bin/env python
# -*- coding: utf-8 -*-
[[[cog

import sys

from robocomp_general import config_robocomp
config_information = config_robocomp("/opt/robocomp/share/robocompdsl/robocompdsl_config.json").config
sys.path.append(config_information["pathfiles"]["path2cogapp"])

import cog
def A():
	cog.out('<@@<')
def Z():
	cog.out('>@@>')
def TAB():
	cog.out('<TABHERE>')

from parseCDSL import *
component = CDSLParsing.fromFile(theCDSL)


REQUIRE_STR = """
<TABHERE><TABHERE># Remote object connection for <NORMAL>
<TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE>proxyString = ic.getProperties().getProperty('<NORMAL>Proxy')
<TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE>basePrx = ic.stringToProxy(proxyString)
<TABHERE><TABHERE><TABHERE><TABHERE><LOWER>_proxy = RoboComp<NORMAL>.<NORMAL>Prx.checkedCast(basePrx)
<TABHERE><TABHERE><TABHERE><TABHERE>mprx["<NORMAL>Proxy"] = <LOWER>_proxy
<TABHERE><TABHERE><TABHERE>except Ice.Exception:
<TABHERE><TABHERE><TABHERE><TABHERE>print 'Cannot connect to the remote object (<NORMAL>)', proxyString
<TABHERE><TABHERE><TABHERE><TABHERE>#traceback.print_exc()
<TABHERE><TABHERE><TABHERE><TABHERE>status = 1
<TABHERE><TABHERE>except Ice.Exception, e:
<TABHERE><TABHERE><TABHERE>print e
<TABHERE><TABHERE><TABHERE>print 'Cannot get <NORMAL>Proxy property.'
<TABHERE><TABHERE><TABHERE>status = 1
"""

SUBSCRIBESTO_STR = """
<TABHERE><TABHERE><NORMAL>_adapter = ic.createObjectAdapter("<NORMAL>Topic")
<TABHERE><TABHERE><LOWER>I_ = <NORMAL>I(worker)
<TABHERE><TABHERE><LOWER>_proxy = <NORMAL>_adapter.addWithUUID(<LOWER>I_).ice_oneway()

<TABHERE><TABHERE>subscribeDone = False
<TABHERE><TABHERE>while not subscribeDone:
<TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><LOWER>_topic = topicManager.retrieve("<NORMAL>")
<TABHERE><TABHERE><TABHERE><TABHERE>subscribeDone = True
<TABHERE><TABHERE><TABHERE>except Ice.Exception, e:
<TABHERE><TABHERE><TABHERE><TABHERE>print "Error. Topic does not exist (yet)"
<TABHERE><TABHERE><TABHERE><TABHERE>status = 0
<TABHERE><TABHERE><TABHERE><TABHERE>time.sleep(1)
<TABHERE><TABHERE>qos = {}
<TABHERE><TABHERE><LOWER>_topic.subscribeAndGetPublisher(qos, <LOWER>_proxy)
<TABHERE><TABHERE><NORMAL>_adapter.activate()
"""

PUBLISHES_STR = """
<TABHERE><TABHERE># Create a proxy to publish a <NORMAL> topic
<TABHERE><TABHERE>topic = False
<TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE>topic = topicManager.retrieve("<NORMAL>")
<TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE>pass
<TABHERE><TABHERE>while not topic:
<TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE>topic = topicManager.retrieve("<NORMAL>")
<TABHERE><TABHERE><TABHERE>except IceStorm.NoSuchTopic:
<TABHERE><TABHERE><TABHERE><TABHERE>try:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>topic = topicManager.create("<NORMAL>")
<TABHERE><TABHERE><TABHERE><TABHERE>except:
<TABHERE><TABHERE><TABHERE><TABHERE><TABHERE>print 'Another client created the <NORMAL> topic? ...'
<TABHERE><TABHERE>pub = topic.getPublisher().ice_oneway()
<TABHERE><TABHERE><LOWER>Topic = <NORMAL>Prx.uncheckedCast(pub)
<TABHERE><TABHERE>mprx["<NORMAL>Pub"] = <LOWER>Topic
"""

IMPLEMENTS_STR = """
<TABHERE><TABHERE>adapter = ic.createObjectAdapter('<NORMAL>')
<TABHERE><TABHERE>adapter.add(<NORMAL>I(worker), ic.stringToIdentity('<LOWER>'))
<TABHERE><TABHERE>adapter.activate()
"""
]]]
[[[end]]]

#
# Copyright (C)
[[[cog
A()
import datetime
cog.out(' '+str(datetime.date.today().year))
Z()
]]]
[[[end]]]
 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

# \mainpage RoboComp::
[[[cog
A()
cog.out(component['name'])
]]]
[[[end]]]
#
# \section intro_sec Introduction
#
# Some information about the component...
#
# \section interface_sec Interface
#
# Descroption of the interface provided...
#
# \section install_sec Installation
#
# \subsection install1_ssec Software depencences
# Software dependences....
#
# \subsection install2_ssec Compile and install
# How to compile/install the component...
#
# \section guide_sec User guide
#
# \subsection config_ssec Configuration file
#
# <p>
# The configuration file...
# </p>
#
# \subsection execution_ssec Execution
#
# Just: "${PATH_TO_BINARY}/
[[[cog
A()
cog.out(component['name'])
Z()
]]]
[[[end]]]
 --Ice.Config=${PATH_TO_CONFIG_FILE}"
#
# \subsection running_ssec Once running
#
#
#

import sys, traceback, Ice, IceStorm, subprocess, threading, time, Queue, os, copy

# Ctrl+c handling
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

from PySide import *

from specificworker import *

config_information = config_robocomp("/opt/robocomp/share/robocompdsl/robocompdsl_config.json").config

if config_information["pathfiles"]["path2localrobocomp"] == "":
	print 'path2localrobocomp in config file not set, using the default value /opt/robocomp'
	config_information["pathfiles"]["path2localrobocomp"] = '/opt/robocomp'
if len(config_information["pathfiles"]["path2localrobocomp"]) == "":
	print 'ROBOCOMP environment variable not set! Exiting.'
	sys.exit()


preStr = "-I"+config_information["pathfiles"]["path2localrobocomp"]+"/interfaces/ -I/opt/robocomp/interfaces/ --all "+config_information["pathfiles"]["path2localrobocomp"]+"/interfaces/"
Ice.loadSlice(preStr+"CommonBehavior.ice")
import RoboCompCommonBehavior
[[[cog
for imp in component['imports']:
	module = IDSLParsing.gimmeIDSL(imp.split('/')[-1])
	incl = imp.split('/')[-1].split('.')[0]
	cog.outl('Ice.loadSlice(preStr+"'+incl+'.ice")')
	cog.outl('import '+module['name']+'')
]]]
[[[end]]]


class CommonBehaviorI(RoboCompCommonBehavior.CommonBehavior):
	def __init__(self, _handler, _communicator):
		self.handler = _handler
		self.communicator = _communicator
	def getFreq(self, current = None):
		self.handler.getFreq()
	def setFreq(self, freq, current = None):
		self.handler.setFreq()
	def timeAwake(self, current = None):
		try:
			return self.handler.timeAwake()
		except:
			print 'Problem getting timeAwake'
	def killYourSelf(self, current = None):
		self.handler.killYourSelf()
	def getAttrList(self, current = None):
		try:
			return self.handler.getAttrList(self.communicator)
		except:
			print 'Problem getting getAttrList'
			traceback.print_exc()
			status = 1
			return



if __name__ == '__main__':
[[[cog
	if component['gui'] != "none":
		cog.outl('<TABHERE>app = QtGui.QApplication(sys.argv)')
	else:
		cog.outl('<TABHERE>app = QtCore.QCoreApplication(sys.argv)')
]]]
[[[end]]]
	params = copy.deepcopy(sys.argv)
	if len(params) > 1:
		if not params[1].startswith('--Ice.Config='):
			params[1] = '--Ice.Config=' + params[1]
	elif len(params) == 1:
		params.append('--Ice.Config=config')
	ic = Ice.initialize(params)
	status = 0
	mprx = {}
[[[cog
if len(component['requires']) > 0 or len(component['publishes']) > 0 or len(component['subscribesTo']) > 0:
	cog.outl('<TABHERE>try:')
for rqa in component['requires']:
	if type(rqa) == type(''):
		rq = rqa
	else:
		rq = rqa[0]
	w = REQUIRE_STR.replace("<NORMAL>", rq).replace("<LOWER>", rq.lower())
	cog.outl(w)

try:
	if len(component['publishes']) > 0 or len(component['subscribesTo']) > 0:
		cog.outl("""
<TABHERE><TABHERE># Topic Manager
<TABHERE><TABHERE>proxy = ic.getProperties().getProperty("TopicManager.Proxy")
<TABHERE><TABHERE>obj = ic.stringToProxy(proxy)
<TABHERE><TABHERE>topicManager = IceStorm.TopicManagerPrx.checkedCast(obj)""")
except:
	pass

for pba in component['publishes']:
	if type(pba) == type(''):
		pb = pba
	else:
		pb = pba[0]
	w = PUBLISHES_STR.replace("<NORMAL>", pb).replace("<LOWER>", pb.lower())
	cog.outl(w)

if len(component['requires']) > 0 or len(component['publishes']) > 0 or len(component['subscribesTo']) > 0:
	cog.outl("""<TABHERE>except:
		<TABHERE>traceback.print_exc()
		<TABHERE>status = 1""")
]]]
[[[end]]]


	if status == 0:
		worker = SpecificWorker(mprx)

[[[cog
for ima in component['implements']:
	if type(ima) == type(''):
		im = ima
	else:
		im = ima[0]
	w = IMPLEMENTS_STR.replace("<NORMAL>", im).replace("<LOWER>", im.lower())
	cog.outl(w)


for sto in component['subscribesTo']:
	if type(sto) == type(''):
		st = sto
	else:
		st = sto[0]
	w = SUBSCRIBESTO_STR.replace("<NORMAL>", st).replace("<LOWER>", st.lower())
	cog.outl(w)
]]]
[[[end]]]

#<TABHERE><TABHERE>adapter.add(CommonBehaviorI(<LOWER>I, ic), ic.stringToIdentity('commonbehavior'))

		app.exec_()

	if ic:
		try:
			ic.destroy()
		except:
			traceback.print_exc()
			status = 1
