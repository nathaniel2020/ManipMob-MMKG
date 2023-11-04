# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name: visualization
   Description: 
   Author: aidan
   date: 2023/5/21
-------------------------------------------------
"""
__author__ = 'aidan'

import os

# -*- coding = utf-8 -*-

import yaml
from nltk.corpus import wordnet as wn
import json
from py2neo import Graph, Node, Relationship,NodeMatcher, RelationshipMatcher
from tqdm import tqdm


class SceneGraph(object):
    def __init__(self, config):
        neo4j_config = config['NEO4J']
        self.graph = Graph(neo4j_config['URL'], auth=(neo4j_config['USER'], neo4j_config['PASSWORD']))
        self.graph.delete_all()  # 清空数据库
        self.node_matcher = NodeMatcher(self.graph) # 会自动更新
        self.relationship_matcher = RelationshipMatcher(self.graph)
        self.scene = config['SCENE']
        self.graph_path = os.path.join(config['OUPUT_DIR'], '{}_graph.json'.format(self.scene))

    def create_node(self, label, name):
        node = Node(label, name=name)
        self.graph.create(node)

        return node

    def create_relationship(self, start_node_name, relation, end_node_name):


        start_node = self.node_matcher.match(start_node_name).where(name=start_node_name).first()
        end_node = self.node_matcher.match(end_node_name).where(name=end_node_name).first()
        r= Relationship(start_node, relation, end_node)
        self.graph.create(r)
        return r

    def get_scene_graph(self):
        probase_file = '../data/data-concept-instance-relations.txt'

        concept = []
        with open('/Users/aidan/Learn/Project/之江/Code/SPL/chatGPT/anno/huggingface.json', 'r', encoding='utf-8') as f:
            for line in f:
                l_json = json.loads(line.strip())
                concept.extend(l_json['Answer'].split(','))
        concept = set(list(concept))

        graph = {}
        with open(probase_file, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc='构建场景图谱'):
                l = line.strip().split('\t')
                if l[0] in concept or l[1] in concept:
                    graph[l[0]] = l[1]

        wordnet_graph = {}
        for word in concept:
            word_sets = wn.synsets(word)
            for word_set in word_sets:
                hypernyms = {s.name().split('.')[0]: word for s in word_set.hypernyms()}
                hyponyms = {word: s.name().split('.')[0] for s in word_set.hyponyms()}
                wordnet_graph.update(hypernyms)
                wordnet_graph.update(hyponyms)

        graph.update(wordnet_graph)
        return graph

    def bulid_graph(self):
        graph_data = json.load(open(self.graph_path, 'r', encoding='utf-8'))
        exict_node = []
        for n1_name, n2_names in tqdm(graph_data.items(), 'visualization'):
            # n1 = self.node_matcher.match(self.label).where(name=n1_name).first()
            # if n1 == None:
            #     n1 = self.create_node(self.label, n1_name)
            #
            # n2 = self.node_matcher.match(self.label).where(name=n2_name).first()
            # if n2 == None:
            #     n2 = self.create_node(self.label, n2_name)
            #
            # relation = self.relationship_matcher.match((n1, n2)).first()
            # if relation == None:
            #     relation= self.create_relationship(n1_name, 'contain', n2_name)
            if len(n2_names) > 1:
                for n2_name in n2_names:
                    if n1_name not in exict_node:
                        n1 = self.create_node(n1_name, n1_name)
                        exict_node.append(n1_name)
                    if n2_name not in exict_node:
                        n2 = self.create_node(n2_name, n2_name)
                        exict_node.append(n2_name)
                    relation = self.create_relationship(n1_name, 'contain', n2_name)


if __name__ == '__main__':
    with open('config.yaml', encoding='utf-8') as f:  # demo.yaml内容同上例yaml字符串
        config = yaml.safe_load(f)
    graph = SceneGraph(config)
    graph.bulid_graph()


