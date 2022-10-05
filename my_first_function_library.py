import os
import glob
import math
import random
from psychopy import core, visual, prefs, event, gui,misc, data
from psychopy import sound


def create_directories(directories):
    if not isinstance(directories,list):
        directories=[directories]        
    for cur_directory in directories:
        if not os.path.exists(cur_directory):
            try:
                os.makedirs(cur_directory)
            except:
                print("could not create", cur_directory)

 
def import_trials (trial_filename, col_names=None, separator=','):
    trial_file = open(trial_filename, 'r')
 
    if col_names is None:
        # Assume the first row contains the column names
        col_names = trial_file.readline().rstrip().split(separator)
    trials_list = []
    for cur_trial in trial_file:
        cur_trial = cur_trial.rstrip().split(separator)
        print(col_names, cur_trial, len(cur_trial), len(col_names))
        assert len(cur_trial) == len(col_names) # make sure the number of column names = number of columns
        trial_dict = dict(zip(col_names, cur_trial))
        trials_list.append(trial_dict)
    return trials_list



def write_data(f,list_to_write,sep=","):
    string_to_write = sep.join(map(str,list_to_write))
    f.write(string_to_write+'\n')


def import_trials_with_header(trialsFilename, colNames=None, separator='\t', header=True,check_lengths=True):
    try:
        trialsFile = open(trialsFilename, 'r')
    except IOError:
        print(trialsFilename, 'is not a valid file')
    
    if colNames is None: # Assume the first row contains the column names
        colNames = trialsFile.readline().rstrip().split(separator)
    trialsList = []
    for trialStr in trialsFile:
        trialList = trialStr.rstrip().split(separator)
        if check_lengths:
            assert len(trialList) == len(colNames)
        trialDict = dict(list(zip(colNames, trialList)))
        trialsList.append(trialDict)
    if header:
        return (colNames, trialsList)
    else:
        return trialList

def basic_load_files(directory,extension,win='',restriction='*'):
    """ Loads all the pictures (or narrowed by the restriction argumnt) in the provided directory.
    Need to pass in the Psychopy window (win) object so that it can be used for loading them in.
    Returns a dictionary with references to the loaded images
    """
    file_list = glob.glob(os.path.join(directory,restriction+extension))
    images = {} #initialize fileMatrix  as a dict because it'll be accessed by file names (picture names, sound names)
    for cur_file in file_list:
        stim_filename = os.path.splitext(os.path.basename(cur_file))[0] #just the filename without the extension
        stim = visual.ImageStim(win, image=cur_file,mask=None,interpolate=True)
        images[stim_filename] = stim
 
    return images


def popupError(text):
    errorDlg = gui.Dlg(title="Error", pos=(400,400))
    errorDlg.addText('Error: '+text, color='Red')
    errorDlg.show()
    

def get_runtime_vars(varsToGet,order,expName):
    """Get run time variables, see http://www.psychopy.org/api/gui.html for explanation"""
    order.append('expName')
    varsToGet['expName']= expName
    try:
        previousRunTime = misc.fromFile(expName+'_lastParams.psydat')
        for curVar in list(previousRunTime.keys()):
            if isinstance(varsToGet[curVar],list) or curVar=="room" or curVar=="date_time":
                pass #don't load it in
            else:
                varsToGet[curVar] = previousRunTime[curVar]
    except:
        pass

    if 'room' in varsToGet and 'date_time' in varsToGet:
        infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=['room','date_time'],order=order)
    else:
        infoDlg = gui.DlgFromDict(dictionary=varsToGet, title=expName, fixed=[expName],order=order)    

    misc.toFile(expName+'_lastParams.psydat', varsToGet)
    if infoDlg.OK:
        return varsToGet
    else: print('User Cancelled')

def open_output_file(subjCode,suffix):
    if  os.path.isfile(subjCode+'_'+suffix+'.txt'):
        popupError('Error: That subject code already exists')
        return False
    else:
        try:
            outputFile = open(subjCode+'_'+suffix+'.txt','w')
        except:
            print('could not open file for writing')
        return outputFile



def draw_and_show(win,stimuli,duration=0):
    """Stimuli can be a list or a single draw-able stimulus"""
    if isinstance(stimuli,list):
        for cur_stim in stimuli:
            cur_stim.draw()
    else:
        stimuli.draw()
    if duration==0: #single frame
        win.flip()
    else: 
        win.flip()
        core.wait(duration)
    return


def get_keyboard_response(validResponses,duration=0):
    event.clearEvents()
    responded = False
    done = False
    rt = '*'
    responseTimer = core.Clock()
    while True: 
        if not responded:
            responded = event.getKeys(keyList=validResponses, timeStamped=responseTimer) 
        if duration>0:
            if responseTimer.getTime() > duration:
                break
        else: #end on response
            if responded:
                break
    if not responded:
        return ['NA','NA']
    else:
        return responded[0] #only get the first resp



def get_mouse_response(mouse,duration=0):
    event.clearEvents()
    responseTimer = core.Clock()
    numButtons=len(event.mouseButtons)
    response = [0]*numButtons
    timeElapsed = False
    mouse.clickReset()
    responseTimer.reset()
    rt = '*'
    while not any(response) and not timeElapsed:
        (response,rt) = mouse.getPressed(getTime=True)
        if duration>0 and responseTimer.getTime() > duration:
            timeElapsed=True
    
    if not any(response): #if there was no response (would only happen if duration is set)
        return ('NA','NA')
    else:
        nonZeroResponses = [x for x in rt if x>0]
        firstResponseButtonIndex = rt.index(min(nonZeroResponses)) #only care about the first (earliest) click
        return (firstResponseButtonIndex,rt[firstResponseButtonIndex])


def write_to_file(fileHandle,trial,separator=',', sync=True,add_newline=False):
    """Writes a trial (array of lists) to a previously opened file"""
    trial = map(str,trial)
    line = separator.join([str(i) for i in trial]) #join with separator
    if add_newline:
        line += '\n' #add a newline
    try:
        fileHandle.write(line)
    except:
        print('file is not open for writing')
    if sync:
        fileHandle.flush()
        os.fsync(fileHandle)
            


def basic_load_files(directory,extension,win='',restriction='*'):
    """ Loads all the pictures (or narrowed by the restriction argumnt) in the provided directory.
    Need to pass in the Psychopy window (win) object so that it can be used for loading them in.
    Returns a dictionary with references to the loaded images
    """
    file_list = glob.glob(os.path.join(directory,restriction+extension))
    images = {} #initialize fileMatrix  as a dict because it'll be accessed by file names (picture names, sound names)
    for cur_file in file_list:
        stim_filename = os.path.splitext(os.path.basename(cur_file))[0] #just the filename without the extension
        stim = visual.ImageStim(win, image=cur_file,mask=None,interpolate=True)
        images[stim_filename] = stim
 
    return images


def load_files(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
    """ Load all the pics and sounds. Uses pyo or pygame for the sound library (see prefs.general['audioLib'])"""
    path = os.getcwd() #set path to current directory
    if isinstance(extension,list):
        fileList = []
        for curExtension in extension:
            fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
    else:
        fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
    files_data = {} #initialize files_data  as a dict because it'll be accessed by file names (picture names, sound names)
    for num,curFile in enumerate(fileList):
        fullPath = curFile
        fullFileName = os.path.basename(fullPath)
        stimFile = os.path.splitext(fullFileName)[0]
        if fileType=="image":
            try:
                surface = pygame.image.load(fullPath) #gets height/width of the image
                stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
                (width,height) = (surface.get_width(),surface.get_height())
            except: #if no pygame, image dimensions may not be available
                pass
            stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
            (width,height) = (stim.size[0],stim.size[1])
            files_data[stimFile] = {'stim':stim,'fullPath':fullFileName,'filename':stimFile,'num':num,'width':width, 'height':height}
        elif fileType=="sound":
            files_data[stimFile] = {'stim':sound.Sound(fullPath), 'duration':sound.Sound(fullPath).getDuration()}
 
    #optionally check a list of desired stimuli against those that've been loaded
    if stimList and set(files_data.keys()).intersection(stimList) != set(stimList):
        popupError(str(set(stimList).difference(list(files_data.keys()))) + " does not exist in " + path+'\\'+directory) 
    return files_data
    
    
    





            
            
            