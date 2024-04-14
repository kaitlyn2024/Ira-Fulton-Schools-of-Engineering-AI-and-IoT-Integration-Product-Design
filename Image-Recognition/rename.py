import os

def rename(path):
    names=[]
    index=0

    for (root, dirs, files) in os.walk(path):
        if index==0:
            names=dirs
        for i, file in enumerate(files):
            new_name = names[index-1]+file;
            os.rename(os.path.join(root, file), os.path.join(root, new_name))
            print(os.path.join(root, file))
        index=index+1

rename(r'~/Desktop/Ira-Fulton-Schools-of-Engineering-AI-and-IoT-Integration-Product-Design/archive/train')
rename(r'~/Desktop/Ira-Fulton-Schools-of-Engineering-AI-and-IoT-Integration-Product-Design/archive/test')
