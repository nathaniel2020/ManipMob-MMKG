# 3D Grounding

Our manipmob is based on https://github.com/snaredataset/snare.

You can prepare the data as the instruction in the github link.

1. Install the requirements.
    
    ```jsx
    conda create -n manipmob python=3.9
    conda activate manipmob
    conda install --yes -c pytorch pytorch=1.7.1 torchvision cudatoolkit=11.0
    pip install ftfy regex tqdm
    pip install git+https://github.com/openai/CLIP.git
    pip install -r requirements
    ```
    
2. Prepare the data
    
    Download pre-extracted image features, language features from [here](https://drive.google.com/drive/folders/18sKN1MawcCjqQ4nbe6m4XAcWogWClKGe) and put them in the data/ folder.
    
3. Prepare the checkpoint and knowledge base
    
    The checkpoint and knowledge base are save in [3D_grounding_manipmob](https://hkustgz-my.sharepoint.com/:f:/g/personal/psun012_connect_hkust-gz_edu_cn/EgbEKRtI4g5GvLorbx9X4lsBn5BAcvxQqUvf9gTmkSWcDQ?e=Zabtdd) and you can download them.
    
4. Run the test scripts
    
    ```jsx
    python val.py train.model=single_cls_kg
    ```
    
5. Run the train scripts
    
    ```jsx
    python train.py train.model=single_cls_kg
    ```
