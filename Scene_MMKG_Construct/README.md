# Schema Construction

1. follow this (repo)[[https://github.com/lm-sys/FastChat](https://github.com/lm-sys/FastChat)] to install the backbone model
    1. install the packages 
        
        ```jsx
        conda create -n scene_mmkg python=3.9
        conda activate scene_mmkg
        pip3 install "fschat[model_worker,webui]"
        pip3 install sentence_transformers
        pip3 install py2neo
        ```
        
    2. RESTful API Server
        
        First, launch the controller
        
        ```
        python3 -m fastchat.serve.controller
        ```
        
        Then, launch the model worker(s)
        
        ```
        python3 -m fastchat.serve.model_worker --model-path lmsys/vicuna-7b-v1.5
        ```
        
        Finally, launch the RESTful API server
        
        ```
        python3 -m fastchat.serve.openai_api_server --host localhost --port 8000
        ```
        
        Now, let us test the API server.
        
    3. install the packages
        
        ```jsx
        pip install --upgrade openai
        ```
        
2. modify configuration file (config.yaml) related information
3. run `preprocess.py`
    
    preprocess the raw Probase (you can download it from [schema_extraction](https://hkustgz-my.sharepoint.com/:f:/g/personal/psun012_connect_hkust-gz_edu_cn/EqwGBXBpN7BEowePDd8UT04Bfs7E4yQpgDfjQLohQ9J2RA?e=fmFHya)) into the dict 
    
    we also provide the processed data “probase.json” from [schema_extraction](https://hkustgz-my.sharepoint.com/:f:/g/personal/psun012_connect_hkust-gz_edu_cn/EqwGBXBpN7BEowePDd8UT04Bfs7E4yQpgDfjQLohQ9J2RA?e=fmFHya).
    
4. run `construct.py` and get the domain graph in your output dir