import os
import pandas as pd
import random
import glob

def generate_trials(subj_vars):
    """Accepts runtime variables and generates appropriate trials"""
    names = list(pd.read_csv('https://raw.githubusercontent.com/psych750/resources/main/stimuli/psych750_roster.csv')['Name'])
    image_files = glob.glob(os.path.join('images','*.png'))
    just_filenames = [os.path.splitext(os.path.basename(cur_file))[0] for cur_file in image_files] #just the filename without the extension

    print(names)
    print(just_filenames)

    for cur_trial in range(int(subj_vars['num_blocks'])):
        random.shuffle(names)
        random.shuffle(just_filenames)
        for cur_name in names:
            print(cur_name) #you'll need to change this so that the relevant information is written to a CSV file. 

if __name__=="__main__":
    generate_trials({'subj_code':'test_subj', 'num_blocks':3})