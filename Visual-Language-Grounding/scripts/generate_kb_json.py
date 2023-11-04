import pickle
import numpy as np
import json
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union
import os
from sentence_transformers import SentenceTransformer, util
import torch
from tqdm import tqdm
model = SentenceTransformer("all-MiniLM-L6-v2")

if __name__ == '__main__':
    json_path = ["/media/air/hard_2/snare/snare/amt/folds_adversarial/train.json",
                 "/media/air/hard_2/snare/snare/amt/folds_adversarial/val.json",
                 "/media/air/hard_2/snare/snare/amt/folds_adversarial/test.json", ]

    annotation_list = set()
    for json_item in json_path:
        json_item = json.load(open(json_item, "r"))
        for _item in json_item:
            annotation_list.add(_item["annotation"])
    annotation_list = list(annotation_list)

    with open("KB/data/entities.txt", "w") as f:
        f.write("\n".join(annotation_list))

    after_augment_json_path = "/media/air/hard_2/IKEA/after_augment/"
    json_dict = {}
    picture_dict = {}
    for item_path in os.listdir(after_augment_json_path):
        with open(after_augment_json_path + item_path, "r", encoding="utf-8") as f:
            after_augment_json_dict = json.load(f)
        json_dict[after_augment_json_dict["name"]] = after_augment_json_dict["affordance"]
        picture_dict[after_augment_json_dict["name"]] = after_augment_json_dict["images"]
    with open("KB/data/entities.txt") as f:
        entity_list = [entity.replace("\n", "") for entity in f.readlines()]
    bert_encoding_value = []
    for name in tqdm(json_dict.keys()):
        bert_encoding_value.append(model.encode(name))

    emb1 = torch.tensor(bert_encoding_value).cuda()
    print(emb1.shape)
    ans_dict = {}
    ans_word = {}
    ans_picture = {}
    ans_dict_path = "KB/ans_dict_v1.json"
    ans_word_path = "KB/ans_word_v1.json"
    ans_picture_path = "KB/ans_picture_v1.json"
    for entity in tqdm(entity_list):
        emb2 = torch.tensor(model.encode(entity)).cuda()
        cos_sim = util.cos_sim(emb1.cuda(), emb2)
        candidate_dict = list(json_dict.values())[torch.argmax(cos_sim).item()]
        candidate_word = list(json_dict.keys())[torch.argmax(cos_sim).item()]
        candidate_picture = list(picture_dict.values())[torch.argmax(cos_sim).item()]
        ans_dict[entity] = candidate_dict
        ans_word[entity] = candidate_word
        ans_picture[entity] = candidate_picture
    with open(ans_dict_path, "w", encoding="utf-8") as f:
        json.dump(ans_dict, f)
    with open(ans_word_path, "w", encoding="utf-8") as f:
        json.dump(ans_word, f)
    with open(ans_picture_path, "w", encoding="utf-8") as f:
        json.dump(ans_picture, f)