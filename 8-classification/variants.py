import os
import random
import math
from shutil import copyfile


def variant_i(p, locs):
    base_path = "data/i/{}".format(p)
    os.makedirs(base_path, exist_ok=True)
    train_dir = 'training'
    valid_dir = 'validation'
    test_dir = 'testing'


    for i in range(len(locs)):
        current_path = "{}/{}".format(base_path, locs[i])
        src_path = "data/{}/{}".format(p, locs[i])
        os.makedirs(current_path, exist_ok=True) 
        for f in os.listdir(src_path):
            dst = "{}/{}".format(current_path, f)
            src = "{}/{}".format(src_path, f)
            copyfile(src, dst)



def other_variants(p, locs):
    dir_names = p.split('/')
    for l in locs:
        path = "{}/{}".format(p, l)
        for f in os.listdir(path):
            with open("{}/{}".format(path, f), 'r') as s_file:
                all_lines = list(s_file)

                variants = [('ii', min(len(all_lines), math.ceil(len(all_lines) / 10))),
                            ('iii', min(len(all_lines), 10)),
                            ('iv', 1)]
                for (i, k) in variants:
                    lines = random.sample(all_lines, k=k)

                    dst = "{}/{}/{}/{}".format(dir_names[0], i, dir_names[1], l)
                    file_path = "{}/{}".format(dst, f)
                    with open(file_path, 'w+') as d_file:
                        for line in lines:
                            d_file.write("%s" % line)
                


def main():
    dir_change = 'zmiana'
    dir_other = 'inne'
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True) 

    train_dir = 'training'
    valid_dir = 'validation'
    test_dir = 'testing'
    locs = [train_dir, valid_dir, test_dir]

    for n in ['i', 'ii', 'iii', 'iv']:
        var_path = "{}/{}".format(data_dir, n)
        os.makedirs(var_path, exist_ok=True)
        for d in [dir_other, dir_change]:
            os.makedirs("{}/{}".format(var_path, d), exist_ok=True)
            for t in locs:
                os.makedirs("{}/{}/{}".format(var_path, d, t), exist_ok=True)

    
	
    variant_i(dir_other, locs)
    variant_i(dir_change, locs)

    other_variants(data_dir + '/' + dir_other, locs)
    other_variants(data_dir + '/' + dir_change, locs)


main()

