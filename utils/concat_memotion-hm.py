"""
train_v10.jsonl includes:
    - train.jsonl (8500)
    - 100 images from 'dev_seen.jsonl' that are not in 'dev_unseen.jsonl' (100)
    - images from memotion dataset (328)
    so in total of 8500+100+328 = 8928 images
"""
import pandas as pd
import argparse
import os

def get_img_list_from_dev(path_to_annotations):
    """
    'dev_seen.jsonl'(0.5k) & 'dev_unseen.jsonl'(0.54k) have 400 identical images.
    This function extracts those 100 images from 'dev_seen.jsonl' that are not in
    'dev_unseen.jsonl' in order to add them into 'train.jsonl' for increasing
    dataset size.

    :param path_to_annotations: Path to annotation .json files
    :return: List of image paths in 'dev_seen.jsonl'
    """
    val_seen = pd.read_json(f"{path_to_annotations}/dev_seen.jsonl", lines=True)["img"]
    val_unseen = pd.read_json(f"{path_to_annotations}/dev_unseen.jsonl", lines=True)["img"]

    diff_ids = list(set(val_seen).symmetric_difference(val_unseen))

    val_seen_imgs = []
    val_unseen_imgs = []
    for img in diff_ids:
        if img in list(val_seen):
            val_seen_imgs.append(img)
        elif img in list(val_unseen):
            val_unseen_imgs.append(img)
        else:
            print("Error occured at img: ", img)

    assert len(val_seen_imgs)==100 , "Error in counting 'dev_seen'"
    assert len(val_unseen_imgs)==140, "Error in counting 'dev_unseen'"
    assert sum([i in list(val_unseen) for i in val_seen_imgs])==0, "Error: some images are in both dev files!"

    return val_seen_imgs


ap = argparse.ArgumentParser()
ap.add_argument("-ho", "--home", required=True, help="home directory of your PC")
args = vars(ap.parse_args())
# Assign corresponding variables
home = args["home"]

# Get annotations
dev_seen = pd.read_json("/root/.cache/torch/mmf/data/datasets/hateful_memes/defaults/annotations/dev_seen.jsonl", lines=True)
dev_unseen = pd.read_json("/root/.cache/torch/mmf/data/datasets/hateful_memes/defaults/annotations/dev_unseen.jsonl", lines=True)
train = pd.read_json("/root/.cache/torch/mmf/data/datasets/hateful_memes/defaults/annotations/train.jsonl", lines=True)

# Get 100 image id's: {'dev_seen' \ 'dev_unseen'}
seen_imgs = get_img_list_from_dev("/root/.cache/torch/mmf/data/datasets/hateful_memes/defaults/annotations/")
# Add 100 images to 'train.jsonl'
for i in seen_imgs:
    train = pd.concat([train, dev_seen[dev_seen["img"]==i]], axis=0)

# Load labeled Memotion data
memotion = pd.read_json(os.path.join(home, "hateful_memes-hate_detectron/utils/label_memotion.jsonl"), lines=True)
# Add memotion data to 'train.jsonl'
train = pd.concat([train, memotion], axis=0)
# Shuffle data
train = train.sample(frac=1).reset_index(drop=True)
# Write new jsonl file
train_json = train.to_json(orient='records', lines=True)

with open(os.path.join(home, "train_v10.jsonl"), "w", encoding='utf-8') as f:
    f.write(train_json)
