import json
from typing import Dict, Union, List

_Relation = Dict[str, Union[str, float]]  # {'@id': str, 'weight': float}
Relation = Dict[str, Union[str, List[_Relation]]]  # {'@id': str, 'related': List[_Relation]}
cache_path = "KB/cache/conceptnet.cache"

with open("KB/ans_dict_v1.json", "r") as f:
    extend_dict = json.load(f)


exist_cache = []
exist_name = set()
def add_cache(obj: Relation):
    exist_cache[obj['@id']] = obj

# with open("/media/air/hard_2/CKR/KB/cache/conceptnet.cache.03312329.ikea", 'r') as cache:
#     for line in cache:
#         obj = json.loads(line)
#         exist_cache.append(obj)
for name, json_dict in extend_dict.items():
    values = []
    ans_dict = None
    for key, item in json_dict.items():
        # {"@id": "/c/en/yolk", "weight": 1.0}
        if f"/c/en/{item.strip()}" == "/c/en/" or f"/c/en/{item.strip()}" == "/c/en/None":
            continue
        if f"/c/en/{item.strip()}".replace(' ', '_') not in values:
            values.append(f"/c/en/{item.strip()}".replace(' ', '_'))

    ans_list = []
    if len(values) == 0:
        continue
    # ans_list.append({"@id": f"/c/en/{name}_clip_image", "weight": 1.0})
    for value in values:
        ans_list.append({"@id": f"{value}", "weight": 1.0})
    if f"/c/en/{name.replace(' ', '_')}" not in exist_name:
        exist_name.add(f"/c/en/{name.replace(' ', '_')}")
        exist_cache.append({"@id": f"/c/en/{name.replace(' ', '_')}", "related":ans_list})
for item in exist_cache:
    with open(cache_path, 'a') as cache:
        json.dump(item, cache)
        cache.write('\n')
        cache.close()