import time
import sys
import random
from psychopy import visual,event,core,gui
from generate_trials import generate_trials


def get_runtime_vars(vars_to_get,order,exp_version="Exercise 3"):
    def popupError(text):
        errorDlg = gui.Dlg(title="Error", pos=(200,400))
        errorDlg.addText('Error: '+text, color='Red')
        errorDlg.show()
        
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    while True:
        infoDlg = gui.DlgFromDict(dictionary=vars_to_get, title=exp_version, order=order,copyDict=True) 
        populated_runtime_vars = infoDlg.dictionary 
        if 'Choose' in list(populated_runtime_vars.values()):
            popupError('Need to choose a value from each dropdown box')
        elif infoDlg.OK:
            return populated_runtime_vars
        elif !infoDlg.OK:
            print('User Cancelled')
            sys.exit()


def write_data(f,list_to_write,sep=","):
    string_to_write = sep.join(map(str,list_to_write))
    f.write(string_to_write+'\n')

win = visual.Window([800,600],color="gray", units='pix')
fixation = visual.TextStim(win,height=40,color="black",text="+")
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])

instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200],autoDraw=True)
feedback_incorrect = visual.TextStim(win,text="INCORRECT", height=40, color="black",pos=[0,0])
feedback_too_slow = visual.TextStim(win,text="TOO SLOW", height=40, color="black",pos=[0,0])
valid_response_keys = ['r', 'o', 'y', 'g', 'b']


# get the runtime variables
order =  ['subj_code','prop_incongruent']
runtime_vars = get_runtime_vars({'subj_code':'stroop_101', 'prop_incongruent':['Choose', '.25','.50', '.75']}, order)

# generate a trial list
generate_trials(runtime_vars['subj_code'], runtime_vars['prop_incongruent'])

#read in generated trial list.
trial_list = open(f"trials/{runtime_vars['subj_code']}_trials.csv",'r').readlines()

#open data file
data_file = open(f"{runtime_vars['subj_code']}_data.csv",'w') 
#works for the exercise, but what problem do you foresee this creating?

response_timer = core.Clock()
for cur_trial_num,cur_trial in enumerate(trial_list):
    trial_data = []
    
    cur_trial = cur_trial.rstrip().split(",") #notice the use of rstrip()
    #grab the trial data for the currnt trial
    subj_code = cur_trial[0]
    prop_incongruent = cur_trial[1]
    cur_word = cur_trial[2]
    cur_color = cur_trial[3]
    cur_trial_type = cur_trial[4]
    cur_orientation = cur_trial[5]
    #notice that this requires us to know which column is which. Not ideal!! How can we do better?


    word_stim.setText(cur_word)
    word_stim.setColor(cur_color)

    #can we avoid this if statement by using a dictionary?
    if cur_orientation=='upside_down':
        word_stim.setOri(180)
    else:
        word_stim.setOri(0)

    fixation.draw()
    win.flip()
    core.wait(.5)
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    placeholder.draw()
    word_stim.draw()
    win.flip()
    response_timer.reset() # start the RT timer here
    key_pressed = event.waitKeys(keyList=valid_response_keys,maxWait=1.5)
    RT = round(response_timer.getTime()*1000,0) # get current time elapsed
    if not key_pressed:
        is_correct = 0
        RT = 'NA'
        feedback_too_slow.draw()
        win.flip()
        core.wait(1)
    elif key_pressed[0] == cur_color[0]:
        is_correct = 1
        #correct response
        pass
    else:
        feedback_incorrect.draw()
        is_correct = 0
        win.flip()
        core.wait(1)
    
    trial_data = [subj_code, cur_trial_num+1] + cur_trial[1:6] +  [is_correct, RT] 
    #make sure you understand what's going on here. Why are we splitting it up into 3 pieces?

    write_data(data_file, trial_data)

data_file.close()
