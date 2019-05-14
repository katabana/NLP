import os
import random
from shutil import copyfile


def copy_files(p, d, sets):
    os.makedirs("{}/{}".format(d, p), exist_ok=True)
    train_dir = 'training'
    valid_dir = 'validation'
    test_dir = 'testing'

    locs = [train_dir, valid_dir, test_dir]

    for i in range(len(locs)):
        os.makedirs("{}/{}/{}".format(d, p, locs[i]), exist_ok=True) 
        for f in sets[i]:
            dst = "{}/{}/{}/{}".format(d, p, locs[i], f)
            src = "{}/{}".format(p, f)
            copyfile(src, dst)


def split_files(p, d):
    # 60% training
    # 20% validation
    # 20% testing

    # choose training set
    k = len(names) * 3 // 5
    train = random.sample(names, k=k)

    # choose validation set
    left_names = [n for n in names if n not in train]
    k = len(left_names) // 2
    valid = random.sample(left_names, k=k)

    # choose testing set
    testing = [n for n in left_names if n not in valid]
    

    copy_files(p, d, [train, valid, testing])


def main():
    dir_change = 'zmiana'
    dir_other = 'inne'
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True) 
    
    split_files(dir_change, data_dir)
    split_files(dir_other, data_dir)




main()

