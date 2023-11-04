# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name: preprocess
   Description: 
   Author: aidan
   date: 2023/5/29
-------------------------------------------------
"""
__author__ = 'aidan'

# preprocess the raw Probase into the dict, we also provide the processed Probase

import yaml
import json
from collections import defaultdict
from tqdm import tqdm
import os

def main(config):
    probase = defaultdict(list)  # 上位-下位
    probase_reverse = defaultdict(list)  # 下位-上位
    with open(config['PROBASE_PATH'], 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc='deal with probase'):
            l = line.strip().split('\t')
            probase[l[0]].append(l[1])
            probase_reverse[l[1]].append(l[0])
    output_dir = config['OUPUT_DIR']
    probase_path = os.path.join(output_dir, 'probase.json')
    probase_reverse_path = os.path.join(output_dir, 'probase_reverse.json')

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    json.dump(probase, open(probase_path, 'w', encoding='utf-8'))
    json.dump(probase_reverse, open(probase_reverse_path, 'w', encoding='utf-8'))

    print('probase deal done.\n')

if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:  # demo.yaml内容同上例yaml字符串
        config = yaml.safe_load(f)
    main(config)
