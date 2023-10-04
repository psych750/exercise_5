import random
from psychopy import core, visual, prefs, event
from my_first_function_library import basic_load_files, draw_and_show, write_to_file, create_directories, calculate_rectangular_coordinates, get_mouse_response, open_data_file, open_trials_file
from generate_trials import generate_trials

data_file = open_data_file('data/sample_data.csv',check_if_exists=False) #this should be done inside the runtime variables collection routine, as in exercise 4


win = visual.Window([1200,820],color="black", units='pix')
myMouse = event.Mouse()
myMouse.setVisible(1)

pics =  basic_load_files('images/','.png',win=win) #only loads all .png files
create_directories(['trials','data'])
coords = calculate_rectangular_coordinates(180, 210, 6, 4, yOffset=0, xOffset=0) #generate a 6x4 grid
name_prompt = visual.TextStim(win,height=60,color="white",text="")


sample_names = ['Zachary Spandler','Andi Donnelly','Fangge Ping', 'Yanchi Liu'] #
#in your solution the above line shouldn't be there; the names are going to be read in from the trials file


def which_image_clicked(coord,pics):
    clicked_images =[]
    for pic_name,image in pics.items():
        if image.contains(coord):
            clicked_images.append(pic_name)
    if len(clicked_images)>1:
        raise Exception("Looks like you have overlapping images and you clicked on an overlap! Boo! Returning 1st one")
    return clicked_images[0]

def compute_accuracy(name_prompt,image_name):
    '''
    Fill in this function so that it returns 1 if the clicked image matches the name; 0 otherwise
    '''
    pass

def present_feedback(is_correct):
    '''
    Fill in this function so that the function shows appropriate correct/incorrect feedback
    A green checkmark for correct and a red cross for incorrect
    The feedback should be shown for 1 second.
    '''
    win.flip()
    pass


def show_trial(name):
    
    random.shuffle(coords)
    trial_data =[]

    #show a name
    name_prompt.setText(name)
    draw_and_show(win,name_prompt,2)

    #iterate through all the images and draw them
    for coord_location,(pic_name,cur_pic) in enumerate(pics.items()): #make sure you understand what's going on here
        cur_pic.setPos([coords[coord_location]]) #set location of each image to one of the coordinates
        cur_pic.draw()
    win.flip()
    (coord,times) = get_mouse_response(myMouse)
    RT = max(times) #because what's being returned is a list of RTs for each mouse button (left, middle, right)
    image_clicked = which_image_clicked(coord,pics)
    is_correct = compute_accuracy(name_prompt,image_clicked)
    present_feedback(is_correct)
    win.flip() #clear screen
    core.wait(2) #inter-trial interval

    trial_data = ['this', 'is', 'your', 'trial', 'data', 'just', 'an', 'example']
    win.flip()
    return(trial_data)
    
for i in range(10):
    trial_data =show_trial(random.choice(sample_names)) #in the actual experimnt you're getting this info from the trial list
    write_to_file(data_file,trial_data,add_newline=True)