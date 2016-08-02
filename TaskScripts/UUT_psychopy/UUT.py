#!/usr/bin/env python
trial_len = 120
# SUPPLIED WITH NO GUARANTEES!!
import os, sys
import numpy as np
from numpy.random import randint, shuffle
from psychopy import visual, core, event, gui, data
#my lazy way of keeping time NB can be relatively inaccurate
import time
from psychopy.misc import fromFile
import csv

_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# set up a stimulus window
myWin = visual.Window(size=(1280, 720),allowGUI=True,winType='pyglet',
            monitor='testMonitor', units ='pix', screen=0)

#set up some fonts. If a list is provided, the first font found will be used.
sans = ['Gill Sans MT', 'Arial','Helvetica','Verdana'] #use the first font found on this list

#INITIALISE SOME STIMULI
#the stimulus could be anything, I'm just using simple text

#collect participant info, create logfile
info = {'Subject':'test'}
infoDlg = gui.DlgFromDict(info, title = 'Subject details:', order = ['Subject'])
#If use clicks OK continue with experiment and create a logfile with their details #else quite experiment
if infoDlg.OK: 
    logpath = 'data\\UUT_%s_%s_log.csv' %(info['Subject'], data.getDateStr())
    f = open(logpath, 'w+') # create log file
#    f.write('%s_%s_%s\n' %(info['Subject'], info['Age'], info['Gender'])) # write participant info
    f.write('Word,CapturedResponseString,EnterAt\n') # write headers
else:
    print 'User Cancelled'
    core.quit()

instrTxt = visual.TextStim(myWin, text='default text', font= sans, units ='pix', name='instruction',
    pos=[-50,0], height=30, wrapWidth=1100,
    color='black',
    ) #object to display instructions
    
def instruction():
    Instruction = open('Instructions\\exp_instr.txt', 'r').read().split('#\n')
    Ready = open('Instructions\\wait_trigger.txt', 'r').read()
    #instructions screen 
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        myWin.flip()
        if i==0:
            core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
        else:
            event.waitKeys(keyList=['return'])

    instrTxt.setText(Ready)
    instrTxt.draw()
    myWin.flip()
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
    
resp_instr = open('Instructions\\resp_instr.txt', 'r').read().split('#\n')

myClock = core.Clock()

#present instructions screen
instruction()
for line in ('SHOES', 'BRICK', 'NEWSPAPER'):
    The_stimulus = visual.TextStim(myWin, 
                            units='norm',height = 0.1,
                            pos=(0, 0), text=line ,
                            font=sans, 
                            alignHoriz = 'center',alignVert='center',
                            color='BlanchedAlmond')

    #acts as a cue for the participant to reponsd
    # shown at the top of the screen
    ResponseInstruction = visual.TextStim(myWin, 
                            units='norm',height = 0.1,
                            pos=(0, 0.5), text=resp_instr[0],
                            font=sans, 
                            alignVert='center',
                            color='BlanchedAlmond')

    #will be used to show the text they are typing: will update every 
    # time they type a letter
    CapturedResponseString = visual.TextStim(myWin, 
                            units='norm',height = 0.1,
                            pos=(0, 0.0), text='',
                            font=sans, 
                            alignHoriz = 'center',alignVert='center',
                            color='BlanchedAlmond')

    captured_string = '' #empty for now.. this is a string of zero length that 
                                     # we will append our key presses to in sequence

    #a routine to save responses to file anytime we want to
    def saveThisResponse(captured_string):
        outfile = "./myResponses.txt"
        f = open(outfile, 'a') #open our results file in append mode so we don't overwrite anything
        f.write(captured_string) #write the string they typed
        f.write('; typed at %s' %time.asctime()) #write a timestamp (very course)
        f.write('\n') # write a line ending
        f.close() #close and "save" the output file
     

    #a routine to update the string on the screen as the participant types
    def updateTheResponse(captured_string):
        CapturedResponseString.setText(captured_string)
        CapturedResponseString.draw()
        ResponseInstruction.draw()
        myWin.flip()


    #setup done, now start doing stuff

    #draw the stimulus .. this can be anything but here it is text
    The_stimulus.draw()  # draw it
    myWin.flip() # show it
    time.sleep(10) #leave it on the screen for 10s
    
    #now instruct the participnat to respond
    ResponseInstruction.draw()  # draw instruction
    myWin.flip() # show instruction
    
    t1 = myClock.getTime()
    event.clearEvents()
    while myClock.getTime() - t1 <= trial_len:
        # now we will keep tracking what's happening on the keyboard
        # until the participant hits the return key
        subject_response_finished = 0 # only changes when they hit return
        
        #check for Esc key / return key presses each frame
        for key in event.getKeys():
                #quit at any point
                if key in ['escape']: 
                    myWin.close()
                    core.quit()
                    
                #if the participant hits return, save the string so far out 
                #and reset the string to zero length for the next trial
                elif myClock.getTime() - t1 >= 120:
                    subject_response_finished = 1 #allows the next trial to start
                    this_captured_string = captured_string.split(',')[-1]
                    if this_captured_string == '':
                        this_captured_string = captured_string.split(',')[-2]
                    f.write('%s,%s,%s\n' %(line, this_captured_string, t3))
                    f.flush()
                    #saveThisResponse(captured_string) #write to file
                    #f.write('%f\n' %(t2))
                    captured_string = '' #reset to zero length 
                    
                    
                #allow the participant to do deletions too , using the 
                # delete key, and show the change they made
                elif key in ['delete','backspace']:
                    captured_string = captured_string[:-1] #delete last character
                    updateTheResponse(captured_string)
                #handle spaces
                elif key in ['space']:
                    captured_string = captured_string+' '
                    updateTheResponse(captured_string)
                elif key in ['period']:
                    captured_string = captured_string+'.'
                    updateTheResponse(captured_string)
                elif key in ['comma']:
                    captured_string = captured_string+','
                    updateTheResponse(captured_string)
                    t2 = myClock.getTime()
                    t3 = t2-t1
                    this_captured_string = captured_string.split(',')[-1]
                    if this_captured_string == '':
                        this_captured_string = captured_string.split(',')[-2]
                    f.write('%s,%s,%s\n' %(line, this_captured_string, t3))
                elif key in ['lshift','rshift']:
                    pass #do nothing when some keys are pressed
                #etc ...

    #if any other key is pressed, add it to the string and 
                # show the participant what they typed
                else: 
                    captured_string = captured_string+key
                    #show it
                    updateTheResponse(captured_string) 
               
####### End of Experiment #####
end_instr = open('Instructions\\end_instr.txt', 'r').read().split('#\n')

finishTxt = visual.TextStim(myWin, units='norm',height = 0.1, text = end_instr[0], 
    font=sans,color='BlanchedAlmond')
finishTxt.draw() 
myWin.flip()
event.waitKeys(maxWait = 20)
core.quit()