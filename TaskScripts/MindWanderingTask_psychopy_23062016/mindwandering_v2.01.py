expName = 'mindwandering_ageing' 
#collect participant info, create logfile
pptInfo = {
    'subject': 'R0001_001', 
    'session': '001', 
    'conditions' : ['random', '0-back', '1-back'],
    } #a pop up window will show up to collect these information

from psychopy import core

from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from MindWandering_TrialDisplay import*
from MindWandering_StimList import*

trials = getTrials(expInfo, datafn, switch=3)
instruction()
myClock = core.Clock()
expTrial(myClock, trials, datafn, expInfo)
