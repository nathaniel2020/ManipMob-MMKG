# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name: construct.py
   Description: 
   Author: aidan
   date: 2023/5/29
-------------------------------------------------
"""
__author__ = 'aidan'

import os

import yaml
import openai
import random
import os
import json
from tqdm import tqdm
from collections import defaultdict
import json
from sentence_transformers import SentenceTransformer, util
import torch
from collections import defaultdict
from tqdm import tqdm


def getSceneDescription(scene, model_name, scene_profile_prompts):
    '''
    use LLM generate scene profile
    :param scene: str
    :param model_name: str
    :param scene_profile_prompts: list of str(prompt)
    :return: str, description of a scene
    '''
    prompt = random.choice(scene_profile_prompts)
    completion = openai.ChatCompletion.create(
        model = model_name,
        messages=[{
            "role": "user",
            "content": prompt.format(scene=scene)
        }]
    )
    return completion.choices[0].message.content


def extractConcepts(desc, model_name, extract_prompts):
    '''
    extract concepts from a text
    :param desc: str, a description of a scene
    :param model_name: str
    :param：extract_prompts: list of str(prompt)
    :return: list of str, concepts list
    '''
    prompt = random.choice(extract_prompts)
    completion = openai.ChatCompletion.create(
        model=model_name,
        messages=[{
            "role": "user",
            "content": prompt.format(desc=desc)
        }]
    )
    content = completion.choices[0].message.content
    concepts = []
    for word in content.split('\n'):
        t = word.split('.')
        if len(t) == 2:
            concept = t[1].strip()
            if concept not in concepts:
                concepts.append(concept)
    return concepts

def main(config):
    scene = '_'.join(config['SCENE'].split())
    output_dir = config['OUPUT_DIR']

    d = {
        'scene': scene,
        'descriptions': []
    }
    for _ in tqdm(range(config['PROFILE_NUM']), desc='Scene Profile'):
        text = getSceneDescription(scene, config['MODEL_NAME'], config['SCENE_PROFILE_PROMPTS'])
        d['descriptions'].append(text)
    profiles_file_name = '{}_profiles.json'.format(scene)
    profiles_file_path = os.path.join(output_dir, profiles_file_name)
    json.dump(d, open(profiles_file_path, 'w', encoding='utf-8'))

    print('Scene Profile already store in [{}]'.format(profiles_file_path))

    profile = json.load(open(profiles_file_path, 'r', encoding='utf-8'))
    d = {
        'scene': scene,
        'concepts': [],
        'desToConcepts': []
    }
    all_concepts = []
    for desc in tqdm(profile['descriptions'], desc='Extract Concepts'):
        concepts = extractConcepts(desc, config['MODEL_NAME'], config['EXTRACT_PROMPTS'])
        d['desToConcepts'].append([desc, concepts])
        all_concepts.extend(concepts)
    d['concepts'] = list(set(all_concepts))

    concepts_file_name = '{}_concepts.json'.format(scene)
    concepts_file_path = os.path.join(output_dir, concepts_file_name)
    json.dump(d, open(concepts_file_path, 'w', encoding='utf-8'))

    print('Conceptes already store in [{}]'.format(concepts_file_path))

    # concepts_file_path = 'output/KFC_concepts.json'
    concepts = json.load(open(concepts_file_path, 'r', encoding='utf-8'))['concepts']
    concepts = [con.lower() for con in concepts]

    probase_path = os.path.join(output_dir, 'probase.json')
    probase_reverse_path = os.path.join(output_dir, 'probase_reverse.json')
    if os.path.exists(probase_path) == False or os.path.exists(probase_reverse_path) == False:
        print('please run preprocess.py firstly')
    else:
        probase = json.load(open(probase_path, 'r', encoding='utf-8'))
        probase_reverse = json.load(open(probase_reverse_path, 'r', encoding='utf-8'))
        graph = defaultdict(list)  # 下位-上位词list
        for (con, ins) in tqdm(probase.items(), desc='construct domain graph'):
            if con in concepts:
                tops = probase_reverse.get(con)
                if tops:
                    graph[con] = tops
                    for top in tops:
                        top_tops = probase_reverse.get(top)
                        if top_tops:
                            graph[top] = top_tops
                downs = probase.get(con)
                if downs:
                    for down in downs:
                        graph[down].append(con)

            elif ins in concepts:
                tops = probase_reverse.get(ins)
                if tops:
                    graph[ins] = tops
                    for top in tops:
                        top_tops = probase_reverse.get(top)
                        if top_tops:
                            graph[top] = top_tops
                downs = probase.get(ins)
                if downs:
                    for down in downs:
                        graph[down].append(ins)


        graph_reverse = defaultdict(list)  # 上-下
        for concept in tqdm(concepts):
            tops = graph.get(concept)
            if tops:
                for top in tops:
                    if concept not in graph_reverse[top]:
                        graph_reverse[top].append(concept)

        graph_reverse_new = defaultdict(list)
        for top, downs in tqdm(graph_reverse.items()):
            if len(downs) > 1:
                graph_reverse_new[top] = downs

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_path = config['SENTENCE_TRANSFORMER_MODEL_PATH']
        model = SentenceTransformer(model_path, device=device)

        words = list(graph_reverse_new.keys())
        words = list(set(words))
        scene_embedding = model.encode(scene, convert_to_tensor=True).to(device)
        word_embeddings = model.encode(words, convert_to_tensor=True).to(device)

        cosine_scores = util.cos_sim(scene_embedding, word_embeddings)
        new_words = []
        for word, sim in zip(words, cosine_scores.tolist()[0]):
            if sim >= 0.4:
                new_words.append(word)

        sim_dict = defaultdict(dict)
        for top in tqdm(new_words):
            downs = graph_reverse_new[top]
            word_embeddings = model.encode(downs, convert_to_tensor=True).to(device)
            cosine_scores = util.cos_sim(scene_embedding, word_embeddings).tolist()[0]
            for word, sim in zip(downs, cosine_scores):
                sim_dict[top][word] = sim

        graph_reverse_new_fifter = defaultdict(list)
        for top in new_words:
            downs = graph_reverse_new[top]
            for word in downs:
                if sim_dict[top][word] >= 0.4:
                    graph_reverse_new_fifter[top].append(word)
        domain_graph_name = '{}_graph.json'.format(scene)
        domain_graph_path = os.path.join(output_dir, domain_graph_name)
        json.dump(graph_reverse_new_fifter, open(domain_graph_path, 'w', encoding='utf-8'))


if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:  # demo.yaml内容同上例yaml字符串
        config = yaml.safe_load(f)

    openai.api_key = config['API_KEY']
    openai.api_base = config['AIP_BASE']

    main(config)