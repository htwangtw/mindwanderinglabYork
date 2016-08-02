expName = 'digitspan_ageing' 
#collect participant info, create logfile
pptInfo = {
    'subject': 'R0001_001', 
    'session': '001', 
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)
f = open_datalog(datafn, dataformat='.csv', headers='condition,index,item,trial,Ans,Resp,corr,RT,IDNO,session\n')


from DigitSpan_TrialDisplay import*

Instruction(block='start')

Instruction(block='F')
myClock = core.Clock()
trials = load_conditions_dict(csvFile='conditions\\digitspanForward.csv')
expTrial(f, myClock, trials, datafn, expInfo, block='F')

Instruction(block='B')
trials = load_conditions_dict(csvFile='conditions\\digitspanBackward.csv')
expTrial(f, myClock, trials, datafn, expInfo, block='B')

endExp(f)
