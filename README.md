# <font color='Aqua'><b> Hateful Memes Challenge-Team HateDetectron Submissions </b></font>

![GitHub Repo stars](https://img.shields.io/github/stars/rizavelioglu/hateful_memes-hate_detectron?style=social)
![GitHub forks](https://img.shields.io/github/forks/rizavelioglu/hateful_memes-hate_detectron?style=social)
![GitHub](https://img.shields.io/github/license/rizavelioglu/hateful_memes-hate_detectron)
![GitHub repo size](https://img.shields.io/github/repo-size/rizavelioglu/hateful_memes-hate_detectron)

Check out the paper on [![arXiv](https://img.shields.io/badge/arXiv-2012.12975-b31b1b.svg)](https://arxiv.org/abs/2012.12975)

This repository contains *all* the code used at the [Hateful Memes Challenge](https://ai.facebook.com/tools/hatefulmemes/) by Facebook AI. There are 2 main Jupyter notebooks where all the job is done and documented:
- The *'reproducing results'* notebook --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kAYFd50XvFnLO-k9FU9iLM21J8djTo-Q?usp=sharing)
- The *'end-to-end'* notebook --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1O0m0j9_NBInzdo3K04jD19IyOhBR1I8i?usp=sharing)

The first notebook is only for reproducing the results of Phase-2 submissions by the team `HateDetectron`. In other words, just loading the final models and getting predictions for the test set. See the [*end-to-end* notebook](https://colab.research.google.com/drive/1O0m0j9_NBInzdo3K04jD19IyOhBR1I8i?usp=sharing) to have a look at the whole approach in detail: how the models are trained, how the image features are extracted, which datasets are used, etc.

---
<h2><b> About the Competition </b></h2>
  The Hateful Memes Challenge and Data Set is a competition and open source data set designed to measure progress in multimodal vision-and-language classification.

  Check out the following sources to get more on the challenge:
  - [Facebook AI](https://ai.facebook.com/tools/hatefulmemes/)
  - [DrivenData](https://www.drivendata.org/competitions/64/hateful-memes/)
  - [Competition Paper](https://arxiv.org/pdf/2005.04790.pdf)

<h3><b> Competition Results: </b></h3>
  We are placed the <b>3rd</b> out of <b>3.173</b> participants in total!

  See the official Leaderboard [here!](https://www.drivendata.org/competitions/70/hateful-memes-phase-2/leaderboard/)

---

<h2><b> Repository structure </b></h2>
  The repository consists of the following folders:

  <details>
  <summary><b><i> hyperparameter_sweep/ </i></b>: where scripts for hyperparameter search are.</summary>

  - `get_27_models.py`: iterates through the folders those that were created for hyperparameter search
    and collects the metrics (ROC-AUC, accuracy) on the 'dev_unseen' set and stores them in a pd.DataFrame. Then, it sorts the models according to AUROC metric and moves the best 27 models into a generated folder `majority_voting_models/`
  - `remove_unused_file.py`: removes unused files, e.g. old checkpoints, to free the disk.
  - `sweep.py`: defines the hyperparameters and starts the process by calling `/sweep.sh`
  - `sweep.sh`: is the mmf cli command to do training on a defined dataset, parameters, etc.

  </details>


  <details>
  <summary><b><i> notebooks/ </i></b>: where Jupyter notebooks are stored.</summary>

  - `[GitHub]end2end_process.ipynb`: presents the whole approach end-to-end: expanding data, image feature extraction, hyperparameter search, fine-tuning, majority voting.
  - `[GitHub]reproduce_submissions.ipynb`: loads our fine-tuned (final) models and generates predictions.
  - `[GitHub]label_memotion.ipynb`: a notebook which uses `/utils/label_memotion.py` to label memes from Memotion and to save it in an appropriate form.
  - `[GitHub]simple_model.ipynb`: includes a simple multimodal model implementation, also known as 'mid-level concat fusion'. We train the model and generate submission for the challenge test set.
  - `[GitHub]benchmarks.ipynb`: reproduces the benchmark results.

  </details>


  <details><summary><b><i> utils/ </i></b>: where some helper scripts are stored, such as labeling Memotion Dataset and merging the two datasets.</summary>

  - `concat_memotion-hm.py`: concatenates the labeled memotion samples and the hateful memes samples and saves them in a new `train.jsonl` file.
  - `generate_submission.sh`: generates predictions for 'test_unseen' set (phase 2 test set).
  - `label_memotion.jsonl`: presents the memes labeled by us from memotion dataset.
  - `label_memotion.py`: is the script for labelling Memotion Dataset. The script iterates over the samples in Memotion and labeler labels the samples by entering 1 or 0 on the keyboard. The labels and the sample metadata is saved at the end as a `label_memotion.jsonl`.

  </details>





---

<h2><b> Citation: </b></h2>

```
@article{velioglu2020hateful,
  author = {Velioglu, Riza and Rose, Jewgeni},
  title = {Detecting Hate Speech in Memes Using Multimodal Deep Learning Approaches: Prize-winning solution to Hateful Memes Challenge},
  doi = {https://doi.org/jhb3}, 
  publisher = {arXiv},
  year = {2020}, 
}
```


<!-- Icons are taken from: https://github.com/edent/SuperTinyIcons -->
<h2><b> Contact: </b></h2>
  <p align="center">
    <a href="http://rizavelioglu.github.io/">
      <img src="logo-1000x500.png" width="300">
    </a>    
    <!-- <a href="https://github.com/rizavelioglu">
      <img src="https://camo.githubusercontent.com/b079fe922f00c4b86f1b724fbc2e8141c468794ce8adbc9b7456e5e1ad09c622/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f6769746875622e737667" width="60">
    </a>
    <a href="https://twitter.com/rizavelioglu">
      <img src="https://camo.githubusercontent.com/35b0b8bfbd8840f35607fb56ad0a139047fd5d6e09ceb060c5c6f0a5abd1044c/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f747769747465722e737667" width="60">
      </a
    <a href="https://www.linkedin.com/in/veliogluriza/">
      <img src="https://camo.githubusercontent.com/c8a9c5b414cd812ad6a97a46c29af67239ddaeae08c41724ff7d945fb4c047e5/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f6c696e6b6564696e2e737667" width="60">
      </a>
    <a href="https://scholar.google.com/citations?user=bEGGmqgAAAAJ&hl=en">
      <img src="https://camo.githubusercontent.com/65ca529d83a419dfbd79954c683f2f928b3e7147433bbfa71f0ddf6824fbe01b/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f7376672f676f6f676c655f7363686f6c61722e737667" width="60">
      </a>
    <a href="https://www.drivendata.org/users/riza.velioglu/">
      <img src="https://drivendata-prod-public.s3.amazonaws.com/images/drivendata-logo.svg" width="250">
    </a> -->
