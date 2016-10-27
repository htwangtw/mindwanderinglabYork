from psychopy import visual, core, event, sound
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*
import os

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
win = set_window(fullscr=True, gui=True, color=1)
fixation = visual.TextStim(win, name='fixation', text='+', color='black', height=62,)#set pix pos
postResp = visual.Circle(win, name='postRespT', lineColor='black', fillColor='black', radius=2, edges=32, )
im = visual.ImageStim(win, name='stimPic', image = None, size = (800, 600), )
msgTxt = visual.TextStim(win,text='default text', font= sans, name='mesage',
    height=34, wrapWidth=1100,
    color='black', 
    )
instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[-50,0], height=30, wrapWidth=1100,
    color='black',
    ) #object to display instructions
play_sound = sound.Sound('A', secs=-1)

Backward_trials = load_conditions_dict(csvFile='conditions\\digitspanBackward.csv')
Forward_trials = load_conditions_dict(csvFile='conditions\\digitspanForward.csv')
CapturedResponseString = visual.TextStim(win, name='participant answer', height=62, text='',
                        font=sans, color='black')

def updateTheResponse(captured_string):
    CapturedResponseString.setText(captured_string)
    CapturedResponseString.draw()
    msgTxt.draw()
    win.flip()

def reset_output():
    keyResp = None
    thisRT = np.nan
    respRT = np.nan
    CORR = np.nan
    return keyResp, thisRT, respRT, CORR

def saveResp(f, i, thisTrial, expInfo, keyResp, respRT, CORR, block):
    write_datalog(f, data='%s,%i,%s,%s,%s,%s,%i,%f,%s,%s\n'
        %(block, i, thisTrial['item'], thisTrial['trial'], thisTrial['correctAns'], 
            keyResp,CORR,respRT,expInfo['subject'],expInfo['session']))
    event.clearEvents()

def Instruction(block='start'):
	if block=='start':
		instruct_txt = open('Instructions\\exp_instr.txt', 'r').read().split('#\n')
	elif block=='F':
		instruct_txt = open('Instructions\\forward_instr.txt', 'r').read().split('#\n')
	elif block=='B':
		instruct_txt = open('Instructions\\backward_instr.txt', 'r').read().split('#\n')
    #instructions screen 
	for i, cur in enumerate(instruct_txt):
	    instrTxt.setText(cur)
	    instrTxt.draw()
	    win.flip()
	    if i==0 and block=='start':
	    	core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
	    else:
	    	event.waitKeys(keyList=['space'])
	    if event.getKeys(keyList = ['escape']):
	        quitEXP(True)
	if block !='start':
		Ready = open('Instructions\\wait_trigger.txt', 'r').read()
		instrTxt.setText(Ready)
		instrTxt.draw()
		win.flip()
	if event.getKeys(keyList = ['escape']):
	    quitEXP(True)
	#need to update a scanner trigger version
	core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])

def fixation_screen(myClock, thisTrial):
	fixation.draw()
	win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
	win.flip()
	fixStart = myClock.getTime() #fixation cross onset
	if event.getKeys(keyList = ['escape']):
		quitEXP(True)
	core.wait(0.5)
	return fixStart


def play_stim(thisTrial):
	fixation.draw()
	win.flip()
	core.wait(0.5)
	for i in range(len(thisTrial['correctAns'])):
		soundfile = 'Stimuli' + os.sep + thisTrial['digit_%i'%(i+1)]
		play_sound.setSound(soundfile)
		play_sound.play()
		core.wait(1)
	event.clearEvents()

def ans_screen(myClock, thisTrial, expInfo, block, f, i):
	if block =='B':
		descrip = open('Instructions\\backward_ans_instr.txt', 'r').read().split('#\n')[0]
	elif block =='F':
		descrip = open('Instructions\\forward_ans_instr.txt', 'r').read().split('#\n')[0]
	msgTxt.setText(descrip)
	msgTxt.draw()
	win.flip()
	win.logOnFlip(level=logging.EXP, msg='Participant answer.') #new log haoting
	startT = myClock.getTime() #stimulus on set
	key, thisRT, respRT, CORR = reset_output()
	captured_string = ''
	CaptureResp = True
	while CaptureResp:
		for key in event.getKeys(keyList=['1', '2', '3', '4', '5', '6', '7', '8', '9', 
											'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', 
											'return', 'backspace', 'escape']):
			# TO DO - make this function to recognise number pad input as normal numbers
			if key == 'return':
				CaptureResp = False
				break
			elif key == 'backspace':
				captured_string = captured_string[:-1]
				updateTheResponse(captured_string)
			elif key == 'escape':
				quitEXP(True)
			else:
				from string import letters, punctuation, digits
				if key in ['num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7', 'num_8', 'num_9', ]: # allow number pad keys
					key = key.translate(None, letters) # no letters
					key = key.translate(None, punctuation) #no underscore
				else: 
					pass
				captured_string += key
				updateTheResponse(captured_string)
	thisRT = myClock.getTime()
	respRT = thisRT-startT
	if captured_string == thisTrial['correctAns']:
		CORR = 1
	else:
		CORR = 0
	saveResp(f, i, thisTrial, expInfo, captured_string, respRT, CORR, block)
	return CORR

def endExp(f):
    endtxt = open('Instructions\\end_instr.txt', 'r').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    f.close()
    win.close()
    core.quit()

def expTrial(f, myClock, trials, datafn, expInfo, block): 
    # keyResp, thisRT, respRT, CORR = reset_output()
    n_corr = 0
    for i, thisTrial in enumerate(trials):
        play_stim(thisTrial)
        x = ans_screen(myClock, thisTrial, expInfo, block, f, i)
        n_corr += x
        print n_corr
        if thisTrial['trial'] =='2':
        	if n_corr==0:
        		break
        	else:
        		n_corr = 0


# endExp(f)


