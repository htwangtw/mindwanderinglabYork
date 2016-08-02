from psychopy import visual, core, event, microphone
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
win = set_window(fullscr=True, gui=True, color=1)
#############################################################################################
instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[-50,0], height=30, wrapWidth=1100,
    color='black',
    ) #object to display instructions

def instruction(inst_txt='Instructions\\exp_encode_instr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('Instructions\\wait_trigger.txt', 'r').read()
    #instructions screen 
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.clearEvents()
        if i==0:
            core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
        else:
            event.waitKeys(keyList=['space'])
    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    if event.getKeys(keyList=['escape']):
        quitEXP(True)
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
    event.clearEvents()

############################################################################################  
fixation = visual.TextStim(win, name='fixation', text='+', 
                            font= sans, height=62, pos=(0,0),color='black')#set pix pos

def fixation_screen(myClock, waittime=1):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    core.wait(waittime)
    return fixStart

##############################################################################################
NART_word = visual.TextStim(win,text='default text', font= sans, name='word',
    height=62, wrapWidth=1100,
    color='black', 
    )

def NART_task(myClock, datafn):
    wavDirName = datafn + '_wav'
    if not os.path.isdir(wavDirName):
        os.makedirs(wavDirName)  # to hold .wav files
    microphone.switchOn()
    mic = microphone.AdvAudioCapture(name='mic', saveDir=wavDirName, stereo=True)
    import codecs 
    stimuli_list = codecs.open('Stimuli\\nart_wordlist.txt', 'r', 'utf-8') .read().split('\n')
    for this in stimuli_list:
        fixation_screen(myClock, waittime=1)
        NART_word.setText(this)
        NART_word.draw()
        win.flip()
        wavfile = mic.record(1200)
        event.waitKeys(keyList=['space'])
        mic.stop()
        if event.getKeys(keyList=['escape']):
            mic.stop()
            quitEXP(True)
##############################################################################################
msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=62, wrapWidth=1100,
    color='black', 
    )

def endExp():
    endtxt = open('Instructions\\end_instr.txt', 'r').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    win.close()
    core.quit()
