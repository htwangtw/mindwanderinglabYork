expName = 'PairedAssociate_ageing' 
#collect participant info, create logfile
pptInfo = {
    'subject': 'R0001_001', 
    'session': '001', 
    'conditions' : ['encoding', 'delayed'],
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from PairedAssociate_TrialDisplay import*
stimuli_list = PairedAssociate_Stimuli()

if expInfo['conditions'] == 'encoding':
    instruction(inst_txt='Instructions\\exp_encode_instr.txt')
    myClock = core.Clock()
    encoding(myClock, stimuli_list)
    instruction(inst_txt='Instructions\\exp_recall_instr.txt')
    f = open_datalog(datafn, dataformat='_immediate.csv', headers='ExpIndex,TrialIndex,target,Ans,Resp,corr,RT(ms),IDNO,session\n')
    myClock = core.Clock()
    recall(myClock, stimuli_list, expInfo, f)
    endExp(f)
    
else:
    instruction(inst_txt='Instructions\\exp_delay_instr.txt')
    f = open_datalog(datafn, dataformat='_delay.csv', headers='ExpIndex,TrialIndex,target,Ans,Resp,corr,RT(ms),RatingResp,RatingRT(ms),IDNO,session\n')
    myClock = core.Clock()
    recall(myClock, stimuli_list, expInfo, f)
    endExp(f) 