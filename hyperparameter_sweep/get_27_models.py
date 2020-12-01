import os
import pandas as pd
import subprocess
from subprocess import call
# Set the following to print the whole dataframe
pd.set_option("display.max_rows", None, "display.max_columns", None)


def get_scores_from_log():
    """
    Iterate through the folders those that were created for hyperparameter search
    and collect the ROC-AUC score as well as the accuracy on the `dev_unseen` set.
    """
    df = pd.DataFrame(columns=['directory', 'ROC-AUC', 'accuracy'])

    for d in os.listdir():
        try:
            if os.path.isdir(d):
                for log in os.listdir(d+"/logs"):
                    if log.endswith("log"):
                        f = open(f"{d+'/logs/'+log}", "r")
                        text = f.read()
                        # get last 250 characters from the log file which captures the score metrics
                        score = text[-250:].split(" ")
                        for idx, i in enumerate(score):
                            if i == 'val/hateful_memes/roc_auc:':
                                roc = score[idx+1].split("\n")[0]
                                acc = score[idx-3].split(",")[0]
                                df.loc[len(df)] = [d, roc, acc]
        except:
            continue

    return df.sort_values(by=['ROC-AUC'], ascending=False)


def move_best_27_models(model_dirs):

    for idx, model in enumerate(model_dirs):
        if not os.path.exists("majority_voting_models"):
            os.mkdir("majority_voting_models")
        print(f"Moving {model+'/best.ckpt'} to majority_voting_models/best-{idx}.ckpt")
        status = call(f"mv {model+'/best.ckpt'} majority_voting_models/best-{idx}.ckpt", shell=True)


sorted_models = get_scores_from_log()
print("[INFO] The results of hyper-parameter tuning: ", sorted_models, "\n")
move_best_27_models(list(sorted_models.head(27)['directory']))
