#!/bin/bash
# https://www.kaggle.com/zengm71/account
# bash DeepFakeChallenge/setup.sh "whateveryourkeyis"
pswd=$1

pip install mmcv
pip install kaggle
pip install RISE
mkdir /root/.kaggle/
touch /root/.kaggle/kaggle.json
chmod 777 /root/.kaggle/kaggle.json
# read -p "Enter Password: " pswd
echo '{"username":"zengm71","key":"'$pswd'"}' > /root/.kaggle/kaggle.json
chmod 600 /root/.kaggle/kaggle.json
kaggle competitions download -c deepfake-detection-challenge
unzip deepfake-detection-challenge.zip -d data
