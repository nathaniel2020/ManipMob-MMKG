# VLN

Our manipmob is based on https://github.com/alloldman/CKR.

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
    
2. Prepare the image features
    
    ```jsx
    wget https://www.dropbox.com/s/o57kxh2mn5rkx4o/ResNet-152-imagenet.zip -P img_features/
    unzip ResNet-152-imagenet.zip
    ```
    
3. Prepare the knowledge base and data from [VLN_manimop](https://hkustgz-my.sharepoint.com/:f:/g/personal/psun012_connect_hkust-gz_edu_cn/EoXSVE2jcXdFoECV2lmiaDYB8GOexogDtwJwL_V_3WP30A?e=FY2icQ). Unzip them into your project.
4. Download the chechpoint from [VLN_manimop](https://hkustgz-my.sharepoint.com/:f:/g/personal/psun012_connect_hkust-gz_edu_cn/EoXSVE2jcXdFoECV2lmiaDYB8GOexogDtwJwL_V_3WP30A?e=FY2icQ).
5. Run the test scripts
    
    ```jsx
    bash run.sh search experiments/results/snapshots/followersample2step_imagenet_mean_pooled_1heads_train_iter_14700val_unseen_sr_0.141_ 0
    ```
    
6. Run the train scripts
    
    ```jsx
    bash run.sh train 0
    ```