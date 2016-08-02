expName = 'NART_ageing' 
#collect participant info, create logfile
pptInfo = {
    'subject': 'R0001_001', 
    'session': '001',
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from NART_TrialDisplay import*

instruction(inst_txt='Instructions\\exp_instr.txt')
myClock = core.Clock()
NART_task(myClock, datafn)
endExp()
