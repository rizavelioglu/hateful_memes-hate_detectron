import os

subfolders= [f.path for f in os.scandir(".") if f.is_dir()]

for i in subfolders:
    os.chdir(f"{i}")
    if os.path.exists("current.ckpt"):
        os.remove("current.ckpt")
    if os.path.exists("visual_bert_final.pth"):
        os.remove("visual_bert_final.pth")
    if os.path.exists("models"):
        os.rmdir("models")
    os.chdir("..")
