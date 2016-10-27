from psychopy import visual, core, event
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
win = set_window(fullscr=True, gui=True, color=1)

msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=62, wrapWidth=1100,
    color='black', 
    )

def PairedAssociate_Stimuli():
    get_encoding_list = open('Stimuli\\learninglist.txt', 'r').read().split('\n')
    stimuli_list = []
    for p in get_encoding_list:
        p_temp = tuple(p.split('-'))
        stimuli_list.append(p_temp)

    from numpy.random import shuffle
    shuffle(stimuli_list)
    return stimuli_list

######################################################################################
#Delay only
question = visual.TextStim(win, name='Question',
   text='On a scale of 1-7, how confident you are about your answer?', font= sans,
   pos=(0,250), height=60, wrapWidth=1300,
   color='black')
#not using the rating scale module
descr = visual.TextStim(win, name='Descriptions',
   text='Not at all                            Completely', font= sans,
   pos=[0, -60], height=50, wrapWidth=1300,
   color='black')
scale = visual.TextStim(win, name='RatingScale',
   text='1      2       3       4       5       6       7', font= sans,
   pos=[0, -120], height=45, wrapWidth=1300,
   color='black', )

def reset_output():
    keyResp = None
    thisRT = np.nan
    respRT = np.nan
    return keyResp, thisRT, respRT

def getResp(startT, myClock):
    keyResp, thisRT, respRT = reset_output()
    while keyResp==None:
        show_questions()
        keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['1', '2', '3', '4', '5', '6', '7', 
                                                                'num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7'])
        if not np.isnan(thisRT):
            respRT = (thisRT - startT) * 1000
        else:
            pass
    return keyResp, respRT

def show_questions():
    question.draw()
    descr.draw()
    scale.draw()
    win.flip()

def Confidence_screen(myClock, thisTrial):
    show_questions()
    win.logOnFlip(level=logging.EXP, msg='Confidence Quesion on screen') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT = getResp(startT, myClock)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    return keyResp, respRT

########################################################################################

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
        if i==0:
        	core.wait(np.arange(2,5,0.5)[randint(0,6)])
        else:
        	event.waitKeys(keyList=['return'])

        if event.getKeys(keyList = ['escape']):
            quitEXP(True)

    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])

############################################################################################  

fixation = visual.TextStim(win, name='fixation', text='+', 
                            font= sans, height=62, pos=(0,0),color='black')#set pix pos

def fixation_screen(myClock, waittime=1):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(waittime)
    return fixStart

##############################################################################################

encodepair = visual.TextStim(win,text='default text', font= sans, name='Encoding word pair',
    height=62, wrapWidth=1100,
    color='black', 
    )

def encoding(myClock, stimuli_list):
    for this in stimuli_list:
        cur_encode = ' - '.join(this)
        fixation_screen(myClock, waittime=1)
        encodepair.setText(cur_encode)
        encodepair.draw()
        win.flip()
        core.wait(5)

##############################################################################################################

Target = visual.TextStim(win, name='target on screen', height=62, pos=(-300,250), wrapWidth=1000, alignHoriz='left',
                        text='test', font=sans, color='black')

def updateTheResponse(captured_string):
    Target.setText(captured_string)
    Target.draw()
    win.flip()

FeedBack = visual.TextStim(win, name='feedback on screen', height=62, pos=(-300,250),
                            text='feedback',
                            font=sans, color='red')
TheAnsIs = visual.TextStim(win,text='The correct answer is', font= sans, name='feedback: correct ans',
                            height=42, pos=(0,100), wrapWidth=1100,
                            color='black',)
ShowCorrAns = visual.TextStim(win, name='show correct ans', height=62, pos=(0,-0),
                            text='feedback',
                            font=sans, color='blue')

def feedback(CORR, captured_string, thisTrial):
    if CORR ==1:
        FeedBack.setText('Correct!')
        FeedBack.draw()
        win.flip()
    elif CORR ==0 and len(captured_string)==0:
        FeedBack.setText('No response detected.')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    else:
        FeedBack.setText('Wrong!')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    core.wait(3)

def ans_screen(myClock, thisTrial, condition, question_length=10):
    fixation_screen(myClock, waittime=1.5)
    event.clearEvents()
    captured_string = ''
    startT = myClock.getTime()
    updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = 0
    respRT = 0
    CORR = 0
    CaptureResp = True
    while CaptureResp and myClock.getTime() - startT <= question_length:
        for key in event.getKeys():
            if key == 'return':
                CaptureResp = False
                break
            elif key == 'backspace':
                captured_string = captured_string[:-1]
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
            elif key == 'escape':
                quitEXP(True)
            elif key in ['lshift','rshift', 'bracketleft', 'bracketright']:
                pass #do nothing when some keys are pressed
            else:
                captured_string += key
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = myClock.getTime()
    respRT = (thisRT-startT) * 1000
    if captured_string == thisTrial[1]:
        CORR = 1
    else:
        CORR = 0
    updateTheResponse(captured_string)
    resp  = captured_string

    if condition == 'encoding':
        feedback(CORR, captured_string, thisTrial)
        return resp, CORR, respRT

    else:
        ratingKey, ratingRT = Confidence_screen(myClock, thisTrial)
        return resp, CORR, respRT, ratingKey, ratingRT

def block_end(countCORR, attempts):
    if countCORR >70:
        # showmessage = 'Your accuracy rate is %f'%(countCORR) + '%' + '. Well done!' + '\n\n\nPess SPACE to continue.'
        showmessage = 'Well done!' + '\n\n\nPess SPACE to continue.'
    else:
        # showmessage = 'Your accuracy rate is %f'%(countCORR) + '%' + '. Good job, but you need to reach 70' + '%' + '. \n\nYou have %i chance(s) left. \n\n\n\nPess SPACE to continue.'%attempts
        showmessage = 'Good job, but you need to try again' + '. \n\nYou have %i chance(s) left. \n\n\n\nPess SPACE to continue.'%attempts
    msgTxt.setText(showmessage)
    msgTxt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def recall(myClock, stimuli_list, expInfo, f):
    fixation.pos = (-300,250)
    continueTest = True
    attempt = 0
    acc = 0

    if expInfo['conditions'] == 'encoding':
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%s\n'
                %(attempt, i, thisTrial[0], thisTrial[1], 
                    resp[0], resp[1], resp[2],
                    expInfo['subject'],expInfo['session']))
            event.clearEvents()
    else:
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%f,%s,%s\n'
                %(attempt, i, thisTrial[0], thisTrial[1], 
                    resp[0], resp[1], resp[2], resp[3], resp[4],
                    expInfo['subject'],expInfo['session']))
            event.clearEvents()
    attempts = 3
    while continueTest and acc < 70:
        countCORR = []
        acc = 0
        attempt +=1
        shuffle(stimuli_list)
        for i, thisTrial in enumerate(stimuli_list):
            if i==21:
                msgTxt.setText('You are half way through this task, if you wish you may take a short break.\n\nPess SPACE to continue.')
                msgTxt.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            else:
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            countCORR.append(resp[1])
            saveResp(f, attempt, i, thisTrial, expInfo, resp)

        acc =  float(sum(countCORR)) / float(len(countCORR)) * 100

        write_datalog(f, data='%i,%s,%s,%s,%s,%i\n'
            %(attempt, 'accuracy', '', '', '', acc))
        if acc >= 70 or attempt == 3:
            block_end(acc, attempts)
            continueTest = False
        elif expInfo['conditions'] == 'delayed':
            continueTest = False
        else:
            attempts -= 1
            block_end(acc, attempts)
            continueTest = True

#############################################################################################################

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
