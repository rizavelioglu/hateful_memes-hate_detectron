import subprocess
from subprocess import call
import os
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-ho", "--home", required=True, help="home directory of your PC")
ap.add_argument("-f", "--feats_dir", required=True, help="directory of features folder")
ap.add_argument("-t", "--train", required=True, help="name of the training .jsonl file")

args = vars(ap.parse_args())
# Assign corresponding variables
home = args["home"]
feats_dir = args["feats_dir"]
train_dir = args["train"]

# for each iteration a folder will be created whose name is 'i'
i = 1

for bs in [32, 64, 80]:
    for lr in [0.3, 0.6]:
        for w_steps in [250, 500]:
            for w_type in ['warmup_cosine', 'warmup_linear']:
                for w_factor in [0.1, 0.3]:
                    for w_iter in [500, 1000]:
                        # call the bash script which start the training
                        rc = call(f"./sweep.sh {str(i)} {lr} {w_steps} {w_type} {w_factor} {w_iter} {bs} {feats_dir} {train_dir}", shell=True)
                        i+=1
