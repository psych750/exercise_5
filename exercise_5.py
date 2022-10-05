import random
from psychopy import core, visual, prefs, event
from my_first_function_library import basic_load_files, write_to_file
from generate_trials import generate_trials

win = visual.Window([800,600],color="black", units='pix')
myMouse = event.Mouse()
myMouse.setVisible(0)

pics =  basic_load_files('stimuli/','.png',restriction="*_*",win=win) #only load .png files with an underscore in them
adjust_stim = visual.GratingStim(win=win,tex='sin', mask='gauss',interpolate=True, size=[8,96], pos=[0,-150], color="white")
myMouse = event.Mouse()
myMouse.setVisible(0)


data_file = open("dummy_data_file.csv","w")

def do_adjustment(pic):
    num_wheel_turns_down=num_wheel_turns_up=0
    responded=False
    while not responded:
        pics[pic].draw()
        adjust_stim.draw()

        wheelRel = myMouse.getWheelRel()[1]
        if wheelRel>0.0:
            num_wheel_turns_down+=1
            print('wheel down: ', num_wheel_turns_up, num_wheel_turns_down)
        elif wheelRel<0.0:
            num_wheel_turns_up+=1
            print('wheel up', num_wheel_turns_up, num_wheel_turns_down)

        #modify the code so that the mouse wheel (trackpad scroll) adjusts the orientation of adjust_stim

        #clicking left mouse button allows you to go to the next trial
        if any(myMouse.getPressed()):
            responded=True
            win.flip()
            core.wait(1)
        trial_data = ['this', 'is', 'your', 'trial', 'data', 'just', 'an', 'example']
        win.flip()
    return(trial_data)
    
for i in range(10):
    trial_data = do_adjustment(random.choice(list(pics.keys()))) #in the actual experimnt you're drawing these from a trial list
    write_to_file(data_file,trial_data,add_newline=True)