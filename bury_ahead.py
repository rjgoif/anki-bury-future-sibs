# # # -*- coding: utf-8 -*-

#########################################################################
# Copyright (C) 2014–2020 by anki/github user rjgoif <https://github.com/rjgoif/>
#                                                                       #
# This program is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation; either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program; if not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

## This add-on will bury all NEW siblings of cards that are due on or before today.
## This way you can get started on your new cards right away when you start your
## daily studies without worrying about them causing overdue cascades: the only
## new cards in your queue will be those that are "daily orphans" (you won't be
## studying their siblings today).

## this only makes sense to do if you have either have your new cards mixed in
## or have them ahead of your reviews. Thus, this add-on will override (WITHOUT
## CHANGING) your deck's settings for when new cards come up. It's important that
## if you normally have new cards last, you leave the actual Anki settings to 
## reflect this. Why? So if you start your daily studying online or iOS (or you 
## disable this addon), it does not totally screw up your burying scheme.


## recommended add-on to use with this one: my "push siblings back" feature.
## (they were made to work together, but "push siblings back" might not be ported yet)
## version 2.1.001 is my first port to Anki 2.1, so my other addons might not be
## ported yet. Also there might be 2.1 bugs. Sorry.

## DOES NOT WORK WITH ANKI 2.0. See my github for a legacy version that you can 
## download and install manually on 2.0 if you're holding on to that version.

# # # # # # # # # # # # # # # #

__version__ = '2.1.001'



import anki
import aqt
import aqt.preferences
import aqt.deckconf
from anki.scheduler import v3
import time
from aqt.utils import showInfo, tooltip
from anki.utils import ids2str, intTime, fmtTimeSpan
from anki.hooks import wrap

from aqt import mw
from aqt.qt import *
from aqt.utils import askUser

userOptions = mw.addonManager.getConfig(__name__)
ahead=userOptions["ahead"]
shortcut=userOptions["shortcut"]
newsAlwaysFirst=userOptions["newsAlwaysFirst"]

def _newCardTime(self):
	"modified from the original to IGNORE the option to put new cards last."
	if not self.newCount:
		return False
	elif self.newCardModulus:
		return self.reps and self.reps % self.newCardModulus == 0
	else:
		return True
if newsAlwaysFirst:
	anki.sched.Scheduler._timeForNewCard = _newCardTime
	
	
# having trouble with the 1000 limit in sqlite/pysql (if a huge list of cards needs to be buried)
# I could loop through all nids, but that will probably be slow.
# instead, will chunk the nids into groups of up to 50.
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]



def buryNewSibsMenu():
	mw.col.save()
	today = int((time.time() - mw.col.crt) // 86400)
	cutoff = today+ahead
	dids = mw.col.decks.allIds()
	didsRevuBury = [0]
	didsNewBury = [0]
	for did in dids:
		conf = mw.col.decks.confForDid(did)
		if not conf["dyn"]:
			if conf["rev"]["bury"]:
				didsRevuBury.append(did)
			if conf["new"]["bury"]:
				didsNewBury.append(did)
	nidsDueToday = set(mw.col.db.list("select nid from cards where queue = 1 or (due <= ? and (queue=2 or queue = 3))", cutoff))
	if not nidsDueToday:
		nidsDueToday = {0}
	nidsRevuToday = set(mw.col.db.list("select nid from cards where id in (select cid from revlog where id>? and type>0)", (mw.col.sched.dayCutoff - 86400)*1000))
	if not nidsRevuToday:
		nidsRevuToday = {0}
	nidsThatBury = nidsDueToday | nidsRevuToday
	chunkedNidsThatBury = chunks(list(nidsThatBury),50)
	for chunk in chunkedNidsThatBury:
		didsThatBuryString = "(" + " or ".join(("did = " + str(did) for did in didsRevuBury)) + ")"
		cidsRevuBury = mw.col.db.list("select id from cards where type = 0 and queue = 0 and " + didsThatBuryString + " and ("
			+ " or ".join(("nid = " + str(nid) for nid in chunk)) + ")")
		nidsNewToday = set(mw.col.db.list("select nid from cards where id in (select cid from revlog where id>? and type=0)", (mw.col.sched.dayCutoff - 86400)*1000))
		didsThatBuryString = "(" + " or ".join(("did = " + str(did) for did in didsNewBury)) + ")"
		if nidsNewToday:
			cidsNewBury = mw.col.db.list("select id from cards where type = 0 and queue = 0 and " + didsThatBuryString + " and ("
			+ " or ".join(("nid = " + str(nid) for nid in nidsNewToday)) + ")")
		else:
			cidsNewBury = [0]
		cidsToBury = list(set(cidsRevuBury + cidsNewBury))
		if cidsToBury:
			mw.col.db.execute(
				"update cards set queue=-2,mod=?,usn=? where id in "+ids2str(cidsToBury),
				intTime(), mw.col.usn())
			mw.col.log(cidsToBury)
	tooltip("Siblings buried prospectively, out "+str(ahead)+" days")



buryNewSibsMenuItem = QAction(mw)
mw.form.menuTools.addAction(buryNewSibsMenuItem)
buryNewSibsMenuItem.setText(_(u"Bury prospective siblings"))
buryNewSibsMenuItem.setShortcut(QKeySequence(shortcut))
buryNewSibsMenuItem.triggered.connect(buryNewSibsMenu)

