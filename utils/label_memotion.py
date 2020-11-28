"""
A program helps to label Memotion Dataset images
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from random import shuffle
import argparse


def plotMemeById(meme_id):
    """
    Plots a meme given its ID.

    - **parameters**::
        :param meme_id: ID of the meme

     Examples:
        >>> plotMemeById("02568")
    """
    # Plot the meme as well as its label
    ext = memo[memo["id"]==int(meme_id)]['img'].values[0].split('.')[1]
    meme_id = int(meme_id) - 100_000
    meme_id = "image_" + str(meme_id)
    fig, axs = plt.subplots(figsize=(10, 6))
    axs.imshow(mpimg.imread(path2img + meme_id + "." + ext))
    axs.set_title(f"Type 'quit' to quit, 'skip' to skip! \n1 for hateful & 0 for not hateful\nMeme ID: {meme_id} ",
                  color="red")
    plt.pause(1)
    plt.show()


def preprocess_text(memo):
    import re
    from collections import Counter

    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text_to_remove = ["imgflip.com", "imgflip", "quickmeme.com", "quickmeme",
                      "memecenter.com", "memecenter", "memegenerator.net",
                      "memegenerator", "9gag.com", "arhtisticlicense.com",
                      "starecat.com", "gapbagap.net", "dudelol.com"]

    pat = r'\b(?:{})\b'.format('|'.join(text_to_remove))

    memo.text = memo.text.str.lower()
    # Remove URLs
    memo.text = memo.text.str.replace(url_pattern, "")
    # Remove words in 'text_to_remove'
    memo.text = memo.text.str.replace(pat, '')
    # Remove any character that's not a letter or a number
    memo.text = memo.text.replace(r"[\W_]+", " ", regex=True)
    memo = memo.dropna()
    return memo


def label_data_and_save(memo):
    continue_labeling = True
    try:
        data = pd.read_json(os.path.join(os.getcwd(), "label_memotion.jsonl"), lines=True)
        if len(data) >= len(memo):
            continue_labeling = False
            return "All data has been labeled!"

        print("[INFO]Found existing file. Loading..")

        ids = list(data["id"])
        idxs = []
        for i in ids:
            idxs.append(memo[memo["id"]==i].index[0])
        memo = memo.drop(idxs)
        test_seen_ids = list(memo["id"])
    except:
        data = pd.DataFrame()
        test_seen_ids = list(memo["id"])
        print("[INFO]Not found an existing file. Creating a new one..")

    shuffle(test_seen_ids)

    while continue_labeling:
        for id in test_seen_ids:
            try:
                _ = plotMemeById(id)
            except:
                continue
            # Preprocess the text in meme
            meme_text = memo[memo['id']==id]['text'].values[0]
            print(meme_text)
            label = input(f"What's the label (saved: {len(data)}): ")

            if label == "quit" or len(data)==1000:
                continue_labeling = False
                plt.close('all')
                break

            elif label == "s":
                continue

            while label not in ["0", "1", "s"]:
                label = input("ERROR: ONLY PUT 1 OR 0: ")

            plt.close('all')

            new_data = memo[memo["id"]==id]
            new_data["label"] = int(label)
            new_data["text"] = meme_text
            data = pd.concat([new_data, data], axis=0)


    # Write new jsonl file
    data = data.to_json(orient='records', lines=True)
    with open(os.path.join(home, "label_memotion.jsonl"), "w", encoding='utf-8') as f:
        f.write(data)


ap = argparse.ArgumentParser()
ap.add_argument("-ho", "--home", required=True, help="home directory of your PC")

args = vars(ap.parse_args())
# Assign corresponding variables
home = args["home"]

path2img = os.path.join(home, "memotion_dataset_7k/images/")
path2data = os.path.join(home, "memotion_dataset_7k/labels.csv")

df = pd.read_csv(path2data, delimiter=',')
nRow, nCol = df.shape
print(f'There are {nRow} rows and {nCol} columns: \n {list(df.columns)}\n')

for i in df["offensive"].unique():
    print(f"# of '{i}' memes \t: {len(df[df['offensive']==i])}")

columns = ["image_name", "text_corrected"]
hateful_offensive = df[df["offensive"]=="hateful_offensive"][columns]
very_offensive    = df[df["offensive"]=="very_offensive"][columns]
not_offensive          = df[df["offensive"]=="not_offensive"][columns]

memo = df[columns]
# Stack the DataFrames on top of each other
# hate = pd.concat([hateful_offensive, very_offensive], axis=0)
# Rename columns
memo.columns = ["id", "text"]
# Add missing columns so it looks like Hateful Memes data
memo["img"] = ("img/" + memo["id"])
memo["img"] = memo["img"].str.lower()
# remove extension in "image_name" & get the number of the image & add 100k
# cause the HM data ID's goes up to 99k
memo["id"] = memo["id"].str.split(".").str.get(0).str.split("_").str.get(1).astype(int) + 100_000
# Re-order columns
memo = memo[["id", "img", "text"]]
# Pre-process the text in memes
memo = preprocess_text(memo)

# Start labeling & save at the end
label_data_and_save(memo)
