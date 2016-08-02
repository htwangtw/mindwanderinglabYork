#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.82.00), 2016_07_07_1618
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'taskswitching.1.820'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'99'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'taskswitching_data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'U:\\TaskScripts\\Task-switching_psychopy-2015-12-14\\taskswitch_141215.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "Instruction"
InstructionClock = core.Clock()
instr = visual.TextStim(win=win, ori=0, name='instr',
    text='Task Switching Task\n\nIn this task, you will first see a cue indicating the relevant dimension.\nThe possible dimensions are: orientation, motion and size.\nNext, you will see four rectangles arranged into a 2x2 matrix display on the screen. \nPlease identify the rectangle that differs from the others regrading the given cue.\nResponses are made on keys that have the same spatial position on the number pad as the rectangles have on the screen.\n\ni.e.\n4 5\n1 2\n\nAfter an incorrect response, an error sign will appear.\n\nThere will be one practice block and two experimental blocks.\n\nPress SPACE to start the practice. ',    font='Arial',
    pos=[0, 0], height=0.05, wrapWidth=0.8,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
#cue-stimulus interval(CSI)
#get digits in the subjet number
subjno =expInfo['participant']
subjno = int(''.join(i for i in subjno if i.isdigit()))

##debug
#print a, subjno, subjno_

if subjno%2==0:
    CSI = [0.1,0.9]
else:
    CSI = [0.9,0.1]

maxrt = 2.5

#select list
seqlist = ['conditions\exp.seq1.xlsx','conditions\exp.seq2.xlsx','conditions\exp.seq3.xlsx','conditions\exp.seq4.xlsx','conditions\exp.seq5.xlsx','conditions\exp.seq6.xlsx']
shuffle(seqlist)
list1 = seqlist[0]
list2 = seqlist[1]

# Initialize components for Routine "Instr_Practice"
Instr_PracticeClock = core.Clock()
start_practice = visual.TextStim(win=win, ori=0, name='start_practice',
    text='Practice',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "READY"
READYClock = core.Clock()
fix = visual.TextStim(win=win, ori=0, name='fix',
    text='+',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()

cue = visual.TextStim(win=win, ori=0, name='cue',
    text='default text',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
frame = visual.Rect(win=win, name='frame',units='cm', 
    width=[8,8][0], height=[8,8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)
neutural = visual.Rect(win=win, name='neutural',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
size = visual.Rect(win=win, name='size',units='cm', 
    width=[1.0, 1.0][0], height=[1.0, 1.0][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
motion = visual.Rect(win=win, name='motion',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-5.0, 
interpolate=True)
orientation = visual.Rect(win=win, name='orientation',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=1.0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-6.0, 
interpolate=True)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
incorrect = visual.TextStim(win=win, ori=0, name='incorrect',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
fbmsg = 'WRONG'
frame_fb = visual.Rect(win=win, name='frame_fb',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)

# Initialize components for Routine "RCI"
RCIClock = core.Clock()
frame_RCI = visual.Rect(win=win, name='frame_RCI',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=0.0, 
interpolate=True)

# Initialize components for Routine "accuracy"
accuracyClock = core.Clock()

msg='doh!'#if this comes up we forgot to update the msg!
blockacc = visual.TextStim(win=win, ori=0, name='blockacc',
    text='default text',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)

# Initialize components for Routine "Instr_exp"
Instr_expClock = core.Clock()
start_exp = visual.TextStim(win=win, ori=0, name='start_exp',
    text='The Real Thing',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "READY"
READYClock = core.Clock()
fix = visual.TextStim(win=win, ori=0, name='fix',
    text='+',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()

cue = visual.TextStim(win=win, ori=0, name='cue',
    text='default text',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
frame = visual.Rect(win=win, name='frame',units='cm', 
    width=[8,8][0], height=[8,8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)
neutural = visual.Rect(win=win, name='neutural',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
size = visual.Rect(win=win, name='size',units='cm', 
    width=[1.0, 1.0][0], height=[1.0, 1.0][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
motion = visual.Rect(win=win, name='motion',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-5.0, 
interpolate=True)
orientation = visual.Rect(win=win, name='orientation',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=1.0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-6.0, 
interpolate=True)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
incorrect = visual.TextStim(win=win, ori=0, name='incorrect',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
fbmsg = 'WRONG'
frame_fb = visual.Rect(win=win, name='frame_fb',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)

# Initialize components for Routine "RCI"
RCIClock = core.Clock()
frame_RCI = visual.Rect(win=win, name='frame_RCI',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=0.0, 
interpolate=True)

# Initialize components for Routine "rest"
restClock = core.Clock()
text_2 = visual.TextStim(win=win, ori=0, name='text_2',
    text='Take a break!\n\nPress SPACE to start the next block.',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)


# Initialize components for Routine "READY"
READYClock = core.Clock()
fix = visual.TextStim(win=win, ori=0, name='fix',
    text='+',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()

cue = visual.TextStim(win=win, ori=0, name='cue',
    text='default text',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
frame = visual.Rect(win=win, name='frame',units='cm', 
    width=[8,8][0], height=[8,8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)
neutural = visual.Rect(win=win, name='neutural',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-3.0, 
interpolate=True)
size = visual.Rect(win=win, name='size',units='cm', 
    width=[1.0, 1.0][0], height=[1.0, 1.0][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=1.0, fillColorSpace='rgb',
    opacity=1,depth=-4.0, 
interpolate=True)
motion = visual.Rect(win=win, name='motion',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-5.0, 
interpolate=True)
orientation = visual.Rect(win=win, name='orientation',units='cm', 
    width=[0.45, 1.5][0], height=[0.45, 1.5][1],
    ori=1.0, pos=[0,0],
    lineWidth=0, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor='blue', fillColorSpace='rgb',
    opacity=1,depth=-6.0, 
interpolate=True)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
incorrect = visual.TextStim(win=win, ori=0, name='incorrect',
    text='default text',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)
fbmsg = 'WRONG'
frame_fb = visual.Rect(win=win, name='frame_fb',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=-2.0, 
interpolate=True)

# Initialize components for Routine "RCI"
RCIClock = core.Clock()
frame_RCI = visual.Rect(win=win, name='frame_RCI',units='cm', 
    width=[8, 8][0], height=[8, 8][1],
    ori=0, pos=[0, 0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=None, fillColorSpace='rgb',
    opacity=1,depth=0.0, 
interpolate=True)

# Initialize components for Routine "end"
endClock = core.Clock()
end_msg = visual.TextStim(win=win, ori=0, name='end_msg',
    text='This is the end of the experiment. Please call the experimenter. ',    font='Arial',
    units='deg', pos=[0, 0], height=1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "Instruction"-------
t = 0
InstructionClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
endInstr = event.BuilderKeyResponse()  # create an object of type KeyResponse
endInstr.status = NOT_STARTED
dis_start=0.5
dis_duration = maxrt+ dis_start
# keep track of which components have finished
InstructionComponents = []
InstructionComponents.append(instr)
InstructionComponents.append(endInstr)
for thisComponent in InstructionComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instruction"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = InstructionClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instr* updates
    if t >= 0.0 and instr.status == NOT_STARTED:
        # keep track of start time/frame for later
        instr.tStart = t  # underestimates by a little under one frame
        instr.frameNStart = frameN  # exact frame index
        instr.setAutoDraw(True)
    
    # *endInstr* updates
    if t >= 0.0 and endInstr.status == NOT_STARTED:
        # keep track of start time/frame for later
        endInstr.tStart = t  # underestimates by a little under one frame
        endInstr.frameNStart = frameN  # exact frame index
        endInstr.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if endInstr.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Instruction"-------
for thisComponent in InstructionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#set next Ntrial
Ntrials = 20
# the Routine "Instruction" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "Instr_Practice"-------
t = 0
Instr_PracticeClock.reset()  # clock 
frameN = -1
routineTimer.add(3.000000)
# update component parameters for each repeat
# keep track of which components have finished
Instr_PracticeComponents = []
Instr_PracticeComponents.append(start_practice)
for thisComponent in Instr_PracticeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instr_Practice"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Instr_PracticeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *start_practice* updates
    if t >= 0.0 and start_practice.status == NOT_STARTED:
        # keep track of start time/frame for later
        start_practice.tStart = t  # underestimates by a little under one frame
        start_practice.frameNStart = frameN  # exact frame index
        start_practice.setAutoDraw(True)
    if start_practice.status == STARTED and t >= (0.0 + (3-win.monitorFramePeriod*0.75)): #most of one frame period left
        start_practice.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instr_PracticeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Instr_Practice"-------
for thisComponent in Instr_PracticeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "READY"-------
t = 0
READYClock.reset()  # clock 
frameN = -1
routineTimer.add(1.400000)
# update component parameters for each repeat
# keep track of which components have finished
READYComponents = []
READYComponents.append(fix)
for thisComponent in READYComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "READY"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = READYClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fix* updates
    if t >= 0.0 and fix.status == NOT_STARTED:
        # keep track of start time/frame for later
        fix.tStart = t  # underestimates by a little under one frame
        fix.frameNStart = frameN  # exact frame index
        fix.setAutoDraw(True)
    if fix.status == STARTED and t >= (0.0 + (1.4-win.monitorFramePeriod*0.75)): #most of one frame period left
        fix.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in READYComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "READY"-------
for thisComponent in READYComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
practice = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('conditions\\practice.seq.xlsx'),
    seed=None, name='practice')
thisExp.addLoop(practice)  # add the loop to the experiment
thisPractice = practice.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisPractice.rgb)
if thisPractice != None:
    for paramName in thisPractice.keys():
        exec(paramName + '= thisPractice.' + paramName)

for thisPractice in practice:
    currentLoop = practice
    # abbreviate parameter names if possible (e.g. rgb = thisPractice.rgb)
    if thisPractice != None:
        for paramName in thisPractice.keys():
            exec(paramName + '= thisPractice.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #reset
    
    order = [0,1,2,3]
    stim_loc = [[-2,-2],[2,-2],[2,2],[-2,2]]
    key = ['num_1','num_2','num_5','num_4']
    mot_dev = [0,1]
    #0->horizontal, 1->vertical
    #col_dev = ['deeppink','purple']
    size_dev = [[1.3,2.1],[0.2,0.7]]
    ori_dev = [45,-45]
    dim = ['motion','orientation','size']
    #################################################
    
    #get cue
    ##temporarily randomised
    #shuffle(dim)
    dim_cue = dim[seq]
    
    ###################################################3
    
    
    
    
    #set display array of the current trial
    shuffle(order)
    mot_loc = stim_loc[order[2]]
    
    shuffle(mot_dev)
    a=mot_loc[mot_dev[0]]
    
    shuffle(size_dev)
    
    shuffle(ori_dev)
    
    #set ans of the current trial
    if dim_cue =='size':
        ans = key[order[1]]
    elif dim_cue =='motion':
        ans = key[order[2]]
    else:
        ans = key[order[3]]
    
    #save the current array
    trialDisp = {'size':size_dev[0], 'motion':mot_dev[0], 'orientation': ori_dev[0], 
        'neu_loc':key[order[0]],'size_loc':key[order[1]],'mot_loc':key[order[2]],'ori_loc':key[order[3]],
        'dimension':dim_cue
        }
    cue.setText(dim_cue)
    neutural.setPos(stim_loc[order[0]])
    size.setFillColor('blue')
    size.setPos(stim_loc[order[1]])
    size.setSize(size_dev[0])
    orientation.setPos(stim_loc[order[3]])
    orientation.setOri(ori_dev[0])
    resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    resp.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(cue)
    trialComponents.append(frame)
    trialComponents.append(neutural)
    trialComponents.append(size)
    trialComponents.append(motion)
    trialComponents.append(orientation)
    trialComponents.append(resp)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        ##SHM
        mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3*3)+a
        #mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3/0.5)+a
        
        ##same speed
        ##not working
        #mot_loc[mot_dev[0]]= a+0.225*(-1)**int(trialClock.getTime()/0.05)
        
        # *cue* updates
        if t >= 0.0 and cue.status == NOT_STARTED:
            # keep track of start time/frame for later
            cue.tStart = t  # underestimates by a little under one frame
            cue.frameNStart = frameN  # exact frame index
            cue.setAutoDraw(True)
        if cue.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            cue.setAutoDraw(False)
        
        # *frame* updates
        if t >= 0.0 and frame.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame.tStart = t  # underestimates by a little under one frame
            frame.frameNStart = frameN  # exact frame index
            frame.setAutoDraw(True)
        if frame.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame.setAutoDraw(False)
        
        # *neutural* updates
        if t >= dis_start and neutural.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutural.tStart = t  # underestimates by a little under one frame
            neutural.frameNStart = frameN  # exact frame index
            neutural.setAutoDraw(True)
        if neutural.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            neutural.setAutoDraw(False)
        
        # *size* updates
        if t >= dis_start and size.status == NOT_STARTED:
            # keep track of start time/frame for later
            size.tStart = t  # underestimates by a little under one frame
            size.frameNStart = frameN  # exact frame index
            size.setAutoDraw(True)
        if size.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            size.setAutoDraw(False)
        
        # *motion* updates
        if t >= dis_start and motion.status == NOT_STARTED:
            # keep track of start time/frame for later
            motion.tStart = t  # underestimates by a little under one frame
            motion.frameNStart = frameN  # exact frame index
            motion.setAutoDraw(True)
        if motion.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            motion.setAutoDraw(False)
        if motion.status == STARTED:  # only update if being drawn
            motion.setPos(mot_loc, log=False)
        
        # *orientation* updates
        if t >= dis_start and orientation.status == NOT_STARTED:
            # keep track of start time/frame for later
            orientation.tStart = t  # underestimates by a little under one frame
            orientation.frameNStart = frameN  # exact frame index
            orientation.setAutoDraw(True)
        if orientation.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            orientation.setAutoDraw(False)
        
        # *resp* updates
        if t >= dis_start and resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            resp.tStart = t  # underestimates by a little under one frame
            resp.frameNStart = frameN  # exact frame index
            resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if resp.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            resp.status = STOPPED
        if resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['num_1', 'num_2', 'num_5', 'num_4'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                resp.keys = theseKeys[-1]  # just the last key pressed
                resp.rt = resp.clock.getTime()
                # was this 'correct'?
                if (resp.keys == str(ans)) or (resp.keys == ans):
                    resp.corr = 1
                else:
                    resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('size',trialDisp['size'])
    thisExp.addData('motion',trialDisp['motion'])
    thisExp.addData('orientation',trialDisp['orientation'])
    thisExp.addData('neu_loc',trialDisp['neu_loc'])
    thisExp.addData('size_loc',trialDisp['size_loc'])
    thisExp.addData('mot_loc',trialDisp['mot_loc'])
    thisExp.addData('ori_loc',trialDisp['ori_loc'])
    thisExp.addData('dimension',trialDisp['dimension'])
    thisExp.addData('CSI',dis_start)
    
    # check responses
    if resp.keys in ['', [], None]:  # No response was made
       resp.keys=None
       # was no response the correct answer?!
       if str(ans).lower() == 'none': resp.corr = 1  # correct non-response
       else: resp.corr = 0  # failed to respond (incorrectly)
    # store data for practice (TrialHandler)
    practice.addData('resp.keys',resp.keys)
    practice.addData('resp.corr', resp.corr)
    if resp.keys != None:  # we had a response
        practice.addData('resp.rt', resp.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    incorrect.setText(fbmsg)
    if resp.corr==1:
        error_disp = 0
    else:
        error_disp = 0.5
    # keep track of which components have finished
    feedbackComponents = []
    feedbackComponents.append(incorrect)
    feedbackComponents.append(frame_fb)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "feedback"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *incorrect* updates
        if t >= 0.0 and incorrect.status == NOT_STARTED:
            # keep track of start time/frame for later
            incorrect.tStart = t  # underestimates by a little under one frame
            incorrect.frameNStart = frameN  # exact frame index
            incorrect.setAutoDraw(True)
        if incorrect.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            incorrect.setAutoDraw(False)
        
        
        # *frame_fb* updates
        if t >= 0.0 and frame_fb.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_fb.tStart = t  # underestimates by a little under one frame
            frame_fb.frameNStart = frameN  # exact frame index
            frame_fb.setAutoDraw(True)
        if frame_fb.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_fb.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "RCI"-------
    t = 0
    RCIClock.reset()  # clock 
    frameN = -1
    routineTimer.add(0.100000)
    # update component parameters for each repeat
    # keep track of which components have finished
    RCIComponents = []
    RCIComponents.append(frame_RCI)
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RCI"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RCIClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *frame_RCI* updates
        if t >= 0.0 and frame_RCI.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_RCI.tStart = t  # underestimates by a little under one frame
            frame_RCI.frameNStart = frameN  # exact frame index
            frame_RCI.setAutoDraw(True)
        if frame_RCI.status == STARTED and t >= (0.0 + (0.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_RCI.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RCIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "RCI"-------
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'practice'


#------Prepare to start Routine "accuracy"-------
t = 0
accuracyClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
dis_start=CSI[0]
dis_duration = maxrt+ dis_start
practice.data['resp.corr']
nCorr = practice.data['resp.corr'].sum() #.std(), .mean() also available
msg = "You got %i out 0f 20 trials correct. Press SPACE to start the next block." %(nCorr)


blockacc.setText(msg)
end_blockfb = event.BuilderKeyResponse()  # create an object of type KeyResponse
end_blockfb.status = NOT_STARTED
# keep track of which components have finished
accuracyComponents = []
accuracyComponents.append(blockacc)
accuracyComponents.append(end_blockfb)
for thisComponent in accuracyComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "accuracy"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = accuracyClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    
    # *blockacc* updates
    if t >= 0.0 and blockacc.status == NOT_STARTED:
        # keep track of start time/frame for later
        blockacc.tStart = t  # underestimates by a little under one frame
        blockacc.frameNStart = frameN  # exact frame index
        blockacc.setAutoDraw(True)
    
    # *end_blockfb* updates
    if t >= 0.0 and end_blockfb.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_blockfb.tStart = t  # underestimates by a little under one frame
        end_blockfb.frameNStart = frameN  # exact frame index
        end_blockfb.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if end_blockfb.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in accuracyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "accuracy"-------
for thisComponent in accuracyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#set next Ntrial
Ntrials = 20
#savelist1
thisExp.addData('list',list1)

# the Routine "accuracy" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "Instr_exp"-------
t = 0
Instr_expClock.reset()  # clock 
frameN = -1
routineTimer.add(3.000000)
# update component parameters for each repeat
# keep track of which components have finished
Instr_expComponents = []
Instr_expComponents.append(start_exp)
for thisComponent in Instr_expComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instr_exp"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Instr_expClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *start_exp* updates
    if t >= 0.0 and start_exp.status == NOT_STARTED:
        # keep track of start time/frame for later
        start_exp.tStart = t  # underestimates by a little under one frame
        start_exp.frameNStart = frameN  # exact frame index
        start_exp.setAutoDraw(True)
    if start_exp.status == STARTED and t >= (0.0 + (3-win.monitorFramePeriod*0.75)): #most of one frame period left
        start_exp.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Instr_expComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Instr_exp"-------
for thisComponent in Instr_expComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "READY"-------
t = 0
READYClock.reset()  # clock 
frameN = -1
routineTimer.add(1.400000)
# update component parameters for each repeat
# keep track of which components have finished
READYComponents = []
READYComponents.append(fix)
for thisComponent in READYComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "READY"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = READYClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fix* updates
    if t >= 0.0 and fix.status == NOT_STARTED:
        # keep track of start time/frame for later
        fix.tStart = t  # underestimates by a little under one frame
        fix.frameNStart = frameN  # exact frame index
        fix.setAutoDraw(True)
    if fix.status == STARTED and t >= (0.0 + (1.4-win.monitorFramePeriod*0.75)): #most of one frame period left
        fix.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in READYComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "READY"-------
for thisComponent in READYComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
block1 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(list1),
    seed=None, name='block1')
thisExp.addLoop(block1)  # add the loop to the experiment
thisBlock1 = block1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock1.rgb)
if thisBlock1 != None:
    for paramName in thisBlock1.keys():
        exec(paramName + '= thisBlock1.' + paramName)

for thisBlock1 in block1:
    currentLoop = block1
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
    if thisBlock1 != None:
        for paramName in thisBlock1.keys():
            exec(paramName + '= thisBlock1.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #reset
    
    order = [0,1,2,3]
    stim_loc = [[-2,-2],[2,-2],[2,2],[-2,2]]
    key = ['num_1','num_2','num_5','num_4']
    mot_dev = [0,1]
    #0->horizontal, 1->vertical
    #col_dev = ['deeppink','purple']
    size_dev = [[1.3,2.1],[0.2,0.7]]
    ori_dev = [45,-45]
    dim = ['motion','orientation','size']
    #################################################
    
    #get cue
    ##temporarily randomised
    #shuffle(dim)
    dim_cue = dim[seq]
    
    ###################################################3
    
    
    
    
    #set display array of the current trial
    shuffle(order)
    mot_loc = stim_loc[order[2]]
    
    shuffle(mot_dev)
    a=mot_loc[mot_dev[0]]
    
    shuffle(size_dev)
    
    shuffle(ori_dev)
    
    #set ans of the current trial
    if dim_cue =='size':
        ans = key[order[1]]
    elif dim_cue =='motion':
        ans = key[order[2]]
    else:
        ans = key[order[3]]
    
    #save the current array
    trialDisp = {'size':size_dev[0], 'motion':mot_dev[0], 'orientation': ori_dev[0], 
        'neu_loc':key[order[0]],'size_loc':key[order[1]],'mot_loc':key[order[2]],'ori_loc':key[order[3]],
        'dimension':dim_cue
        }
    cue.setText(dim_cue)
    neutural.setPos(stim_loc[order[0]])
    size.setFillColor('blue')
    size.setPos(stim_loc[order[1]])
    size.setSize(size_dev[0])
    orientation.setPos(stim_loc[order[3]])
    orientation.setOri(ori_dev[0])
    resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    resp.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(cue)
    trialComponents.append(frame)
    trialComponents.append(neutural)
    trialComponents.append(size)
    trialComponents.append(motion)
    trialComponents.append(orientation)
    trialComponents.append(resp)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        ##SHM
        mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3*3)+a
        #mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3/0.5)+a
        
        ##same speed
        ##not working
        #mot_loc[mot_dev[0]]= a+0.225*(-1)**int(trialClock.getTime()/0.05)
        
        # *cue* updates
        if t >= 0.0 and cue.status == NOT_STARTED:
            # keep track of start time/frame for later
            cue.tStart = t  # underestimates by a little under one frame
            cue.frameNStart = frameN  # exact frame index
            cue.setAutoDraw(True)
        if cue.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            cue.setAutoDraw(False)
        
        # *frame* updates
        if t >= 0.0 and frame.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame.tStart = t  # underestimates by a little under one frame
            frame.frameNStart = frameN  # exact frame index
            frame.setAutoDraw(True)
        if frame.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame.setAutoDraw(False)
        
        # *neutural* updates
        if t >= dis_start and neutural.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutural.tStart = t  # underestimates by a little under one frame
            neutural.frameNStart = frameN  # exact frame index
            neutural.setAutoDraw(True)
        if neutural.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            neutural.setAutoDraw(False)
        
        # *size* updates
        if t >= dis_start and size.status == NOT_STARTED:
            # keep track of start time/frame for later
            size.tStart = t  # underestimates by a little under one frame
            size.frameNStart = frameN  # exact frame index
            size.setAutoDraw(True)
        if size.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            size.setAutoDraw(False)
        
        # *motion* updates
        if t >= dis_start and motion.status == NOT_STARTED:
            # keep track of start time/frame for later
            motion.tStart = t  # underestimates by a little under one frame
            motion.frameNStart = frameN  # exact frame index
            motion.setAutoDraw(True)
        if motion.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            motion.setAutoDraw(False)
        if motion.status == STARTED:  # only update if being drawn
            motion.setPos(mot_loc, log=False)
        
        # *orientation* updates
        if t >= dis_start and orientation.status == NOT_STARTED:
            # keep track of start time/frame for later
            orientation.tStart = t  # underestimates by a little under one frame
            orientation.frameNStart = frameN  # exact frame index
            orientation.setAutoDraw(True)
        if orientation.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            orientation.setAutoDraw(False)
        
        # *resp* updates
        if t >= dis_start and resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            resp.tStart = t  # underestimates by a little under one frame
            resp.frameNStart = frameN  # exact frame index
            resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if resp.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            resp.status = STOPPED
        if resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['num_1', 'num_2', 'num_5', 'num_4'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                resp.keys = theseKeys[-1]  # just the last key pressed
                resp.rt = resp.clock.getTime()
                # was this 'correct'?
                if (resp.keys == str(ans)) or (resp.keys == ans):
                    resp.corr = 1
                else:
                    resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('size',trialDisp['size'])
    thisExp.addData('motion',trialDisp['motion'])
    thisExp.addData('orientation',trialDisp['orientation'])
    thisExp.addData('neu_loc',trialDisp['neu_loc'])
    thisExp.addData('size_loc',trialDisp['size_loc'])
    thisExp.addData('mot_loc',trialDisp['mot_loc'])
    thisExp.addData('ori_loc',trialDisp['ori_loc'])
    thisExp.addData('dimension',trialDisp['dimension'])
    thisExp.addData('CSI',dis_start)
    
    # check responses
    if resp.keys in ['', [], None]:  # No response was made
       resp.keys=None
       # was no response the correct answer?!
       if str(ans).lower() == 'none': resp.corr = 1  # correct non-response
       else: resp.corr = 0  # failed to respond (incorrectly)
    # store data for block1 (TrialHandler)
    block1.addData('resp.keys',resp.keys)
    block1.addData('resp.corr', resp.corr)
    if resp.keys != None:  # we had a response
        block1.addData('resp.rt', resp.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    incorrect.setText(fbmsg)
    if resp.corr==1:
        error_disp = 0
    else:
        error_disp = 0.5
    # keep track of which components have finished
    feedbackComponents = []
    feedbackComponents.append(incorrect)
    feedbackComponents.append(frame_fb)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "feedback"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *incorrect* updates
        if t >= 0.0 and incorrect.status == NOT_STARTED:
            # keep track of start time/frame for later
            incorrect.tStart = t  # underestimates by a little under one frame
            incorrect.frameNStart = frameN  # exact frame index
            incorrect.setAutoDraw(True)
        if incorrect.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            incorrect.setAutoDraw(False)
        
        
        # *frame_fb* updates
        if t >= 0.0 and frame_fb.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_fb.tStart = t  # underestimates by a little under one frame
            frame_fb.frameNStart = frameN  # exact frame index
            frame_fb.setAutoDraw(True)
        if frame_fb.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_fb.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "RCI"-------
    t = 0
    RCIClock.reset()  # clock 
    frameN = -1
    routineTimer.add(0.100000)
    # update component parameters for each repeat
    # keep track of which components have finished
    RCIComponents = []
    RCIComponents.append(frame_RCI)
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RCI"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RCIClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *frame_RCI* updates
        if t >= 0.0 and frame_RCI.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_RCI.tStart = t  # underestimates by a little under one frame
            frame_RCI.frameNStart = frameN  # exact frame index
            frame_RCI.setAutoDraw(True)
        if frame_RCI.status == STARTED and t >= (0.0 + (0.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_RCI.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RCIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "RCI"-------
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block1'


#------Prepare to start Routine "rest"-------
t = 0
restClock.reset()  # clock 
frameN = -1
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()  # create an object of type KeyResponse
key_resp_2.status = NOT_STARTED
dis_start=CSI[1]
dis_duration = maxrt+ dis_start
#savelist2
thisExp.addData('list',list2)
# keep track of which components have finished
restComponents = []
restComponents.append(text_2)
restComponents.append(key_resp_2)
for thisComponent in restComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "rest"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = restClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_2* updates
    if t >= 0.0 and text_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        text_2.tStart = t  # underestimates by a little under one frame
        text_2.frameNStart = frameN  # exact frame index
        text_2.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t  # underestimates by a little under one frame
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in restComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "rest"-------
for thisComponent in restComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
#set next Ntrial
Ntrials = 20

# the Routine "rest" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "READY"-------
t = 0
READYClock.reset()  # clock 
frameN = -1
routineTimer.add(1.400000)
# update component parameters for each repeat
# keep track of which components have finished
READYComponents = []
READYComponents.append(fix)
for thisComponent in READYComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "READY"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = READYClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *fix* updates
    if t >= 0.0 and fix.status == NOT_STARTED:
        # keep track of start time/frame for later
        fix.tStart = t  # underestimates by a little under one frame
        fix.frameNStart = frameN  # exact frame index
        fix.setAutoDraw(True)
    if fix.status == STARTED and t >= (0.0 + (1.4-win.monitorFramePeriod*0.75)): #most of one frame period left
        fix.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in READYComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "READY"-------
for thisComponent in READYComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
block2 = data.TrialHandler(nReps=1, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(list2),
    seed=None, name='block2')
thisExp.addLoop(block2)  # add the loop to the experiment
thisBlock2 = block2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisBlock2.rgb)
if thisBlock2 != None:
    for paramName in thisBlock2.keys():
        exec(paramName + '= thisBlock2.' + paramName)

for thisBlock2 in block2:
    currentLoop = block2
    # abbreviate parameter names if possible (e.g. rgb = thisBlock2.rgb)
    if thisBlock2 != None:
        for paramName in thisBlock2.keys():
            exec(paramName + '= thisBlock2.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    #reset
    
    order = [0,1,2,3]
    stim_loc = [[-2,-2],[2,-2],[2,2],[-2,2]]
    key = ['num_1','num_2','num_5','num_4']
    mot_dev = [0,1]
    #0->horizontal, 1->vertical
    #col_dev = ['deeppink','purple']
    size_dev = [[1.3,2.1],[0.2,0.7]]
    ori_dev = [45,-45]
    dim = ['motion','orientation','size']
    #################################################
    
    #get cue
    ##temporarily randomised
    #shuffle(dim)
    dim_cue = dim[seq]
    
    ###################################################3
    
    
    
    
    #set display array of the current trial
    shuffle(order)
    mot_loc = stim_loc[order[2]]
    
    shuffle(mot_dev)
    a=mot_loc[mot_dev[0]]
    
    shuffle(size_dev)
    
    shuffle(ori_dev)
    
    #set ans of the current trial
    if dim_cue =='size':
        ans = key[order[1]]
    elif dim_cue =='motion':
        ans = key[order[2]]
    else:
        ans = key[order[3]]
    
    #save the current array
    trialDisp = {'size':size_dev[0], 'motion':mot_dev[0], 'orientation': ori_dev[0], 
        'neu_loc':key[order[0]],'size_loc':key[order[1]],'mot_loc':key[order[2]],'ori_loc':key[order[3]],
        'dimension':dim_cue
        }
    cue.setText(dim_cue)
    neutural.setPos(stim_loc[order[0]])
    size.setFillColor('blue')
    size.setPos(stim_loc[order[1]])
    size.setSize(size_dev[0])
    orientation.setPos(stim_loc[order[3]])
    orientation.setOri(ori_dev[0])
    resp = event.BuilderKeyResponse()  # create an object of type KeyResponse
    resp.status = NOT_STARTED
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(cue)
    trialComponents.append(frame)
    trialComponents.append(neutural)
    trialComponents.append(size)
    trialComponents.append(motion)
    trialComponents.append(orientation)
    trialComponents.append(resp)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        ##SHM
        mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3*3)+a
        #mot_loc[mot_dev[0]]= 0.45*sin(trialClock.getTime()%3/0.5)+a
        
        ##same speed
        ##not working
        #mot_loc[mot_dev[0]]= a+0.225*(-1)**int(trialClock.getTime()/0.05)
        
        # *cue* updates
        if t >= 0.0 and cue.status == NOT_STARTED:
            # keep track of start time/frame for later
            cue.tStart = t  # underestimates by a little under one frame
            cue.frameNStart = frameN  # exact frame index
            cue.setAutoDraw(True)
        if cue.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            cue.setAutoDraw(False)
        
        # *frame* updates
        if t >= 0.0 and frame.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame.tStart = t  # underestimates by a little under one frame
            frame.frameNStart = frameN  # exact frame index
            frame.setAutoDraw(True)
        if frame.status == STARTED and t >= (0.0 + (dis_duration-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame.setAutoDraw(False)
        
        # *neutural* updates
        if t >= dis_start and neutural.status == NOT_STARTED:
            # keep track of start time/frame for later
            neutural.tStart = t  # underestimates by a little under one frame
            neutural.frameNStart = frameN  # exact frame index
            neutural.setAutoDraw(True)
        if neutural.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            neutural.setAutoDraw(False)
        
        # *size* updates
        if t >= dis_start and size.status == NOT_STARTED:
            # keep track of start time/frame for later
            size.tStart = t  # underestimates by a little under one frame
            size.frameNStart = frameN  # exact frame index
            size.setAutoDraw(True)
        if size.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            size.setAutoDraw(False)
        
        # *motion* updates
        if t >= dis_start and motion.status == NOT_STARTED:
            # keep track of start time/frame for later
            motion.tStart = t  # underestimates by a little under one frame
            motion.frameNStart = frameN  # exact frame index
            motion.setAutoDraw(True)
        if motion.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            motion.setAutoDraw(False)
        if motion.status == STARTED:  # only update if being drawn
            motion.setPos(mot_loc, log=False)
        
        # *orientation* updates
        if t >= dis_start and orientation.status == NOT_STARTED:
            # keep track of start time/frame for later
            orientation.tStart = t  # underestimates by a little under one frame
            orientation.frameNStart = frameN  # exact frame index
            orientation.setAutoDraw(True)
        if orientation.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            orientation.setAutoDraw(False)
        
        # *resp* updates
        if t >= dis_start and resp.status == NOT_STARTED:
            # keep track of start time/frame for later
            resp.tStart = t  # underestimates by a little under one frame
            resp.frameNStart = frameN  # exact frame index
            resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if resp.status == STARTED and t >= (dis_start + (maxrt-win.monitorFramePeriod*0.75)): #most of one frame period left
            resp.status = STOPPED
        if resp.status == STARTED:
            theseKeys = event.getKeys(keyList=['num_1', 'num_2', 'num_5', 'num_4'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                resp.keys = theseKeys[-1]  # just the last key pressed
                resp.rt = resp.clock.getTime()
                # was this 'correct'?
                if (resp.keys == str(ans)) or (resp.keys == ans):
                    resp.corr = 1
                else:
                    resp.corr = 0
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.addData('size',trialDisp['size'])
    thisExp.addData('motion',trialDisp['motion'])
    thisExp.addData('orientation',trialDisp['orientation'])
    thisExp.addData('neu_loc',trialDisp['neu_loc'])
    thisExp.addData('size_loc',trialDisp['size_loc'])
    thisExp.addData('mot_loc',trialDisp['mot_loc'])
    thisExp.addData('ori_loc',trialDisp['ori_loc'])
    thisExp.addData('dimension',trialDisp['dimension'])
    thisExp.addData('CSI',dis_start)
    
    # check responses
    if resp.keys in ['', [], None]:  # No response was made
       resp.keys=None
       # was no response the correct answer?!
       if str(ans).lower() == 'none': resp.corr = 1  # correct non-response
       else: resp.corr = 0  # failed to respond (incorrectly)
    # store data for block2 (TrialHandler)
    block2.addData('resp.keys',resp.keys)
    block2.addData('resp.corr', resp.corr)
    if resp.keys != None:  # we had a response
        block2.addData('resp.rt', resp.rt)
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock 
    frameN = -1
    # update component parameters for each repeat
    incorrect.setText(fbmsg)
    if resp.corr==1:
        error_disp = 0
    else:
        error_disp = 0.5
    # keep track of which components have finished
    feedbackComponents = []
    feedbackComponents.append(incorrect)
    feedbackComponents.append(frame_fb)
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "feedback"-------
    continueRoutine = True
    while continueRoutine:
        # get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *incorrect* updates
        if t >= 0.0 and incorrect.status == NOT_STARTED:
            # keep track of start time/frame for later
            incorrect.tStart = t  # underestimates by a little under one frame
            incorrect.frameNStart = frameN  # exact frame index
            incorrect.setAutoDraw(True)
        if incorrect.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            incorrect.setAutoDraw(False)
        
        
        # *frame_fb* updates
        if t >= 0.0 and frame_fb.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_fb.tStart = t  # underestimates by a little under one frame
            frame_fb.frameNStart = frameN  # exact frame index
            frame_fb.setAutoDraw(True)
        if frame_fb.status == STARTED and t >= (0.0 + (error_disp-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_fb.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # the Routine "feedback" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    #------Prepare to start Routine "RCI"-------
    t = 0
    RCIClock.reset()  # clock 
    frameN = -1
    routineTimer.add(0.100000)
    # update component parameters for each repeat
    # keep track of which components have finished
    RCIComponents = []
    RCIComponents.append(frame_RCI)
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "RCI"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = RCIClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *frame_RCI* updates
        if t >= 0.0 and frame_RCI.status == NOT_STARTED:
            # keep track of start time/frame for later
            frame_RCI.tStart = t  # underestimates by a little under one frame
            frame_RCI.frameNStart = frameN  # exact frame index
            frame_RCI.setAutoDraw(True)
        if frame_RCI.status == STARTED and t >= (0.0 + (0.1-win.monitorFramePeriod*0.75)): #most of one frame period left
            frame_RCI.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in RCIComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "RCI"-------
    for thisComponent in RCIComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    thisExp.nextEntry()
    
# completed 1 repeats of 'block2'


#------Prepare to start Routine "end"-------
t = 0
endClock.reset()  # clock 
frameN = -1
routineTimer.add(20.000000)
# update component parameters for each repeat
exit_exp = event.BuilderKeyResponse()  # create an object of type KeyResponse
exit_exp.status = NOT_STARTED
# keep track of which components have finished
endComponents = []
endComponents.append(end_msg)
endComponents.append(exit_exp)
for thisComponent in endComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "end"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = endClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end_msg* updates
    if t >= 0.0 and end_msg.status == NOT_STARTED:
        # keep track of start time/frame for later
        end_msg.tStart = t  # underestimates by a little under one frame
        end_msg.frameNStart = frameN  # exact frame index
        end_msg.setAutoDraw(True)
    if end_msg.status == STARTED and t >= (0.0 + (20-win.monitorFramePeriod*0.75)): #most of one frame period left
        end_msg.setAutoDraw(False)
    
    # *exit_exp* updates
    if t >= 0.0 and exit_exp.status == NOT_STARTED:
        # keep track of start time/frame for later
        exit_exp.tStart = t  # underestimates by a little under one frame
        exit_exp.frameNStart = frameN  # exact frame index
        exit_exp.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if exit_exp.status == STARTED and t >= (0.0 + (20-win.monitorFramePeriod*0.75)): #most of one frame period left
        exit_exp.status = STOPPED
    if exit_exp.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in endComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "end"-------
for thisComponent in endComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)










# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort() # or data files will save again on exit
win.close()
core.quit()
