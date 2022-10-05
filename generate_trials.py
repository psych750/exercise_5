import os
import glob

def generate_trials(runtime_vars):
    """Accepts runtime variables and generates appropriate trials"""
    image_files = glob.glob(os.path.join('stimuli','*_*.png'))
    just_filenames = [os.path.splitext(os.path.basename(cur_file))[0] for cur_file in image_files] #just the filename without the extension
    for cur_filename in just_filenames:
        try:
            (displayed_string, orientation, true_angle, tilt_direction) = cur_filename.split('_')
        except ValueError:
            print(cur_filename, 'is not in the right format')
        print(displayed_string, orientation, true_angle, tilt_direction)


if __name__=="__main__":
    generate_trials({'subj_code':'test_subj', 'seed':10, 'num_blocks':1})