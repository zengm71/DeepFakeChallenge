# DeepFakeChallenge

# Setup

## Please see instrcutions on VM and mounting COS bucket in `/data`

## Docker 
    I used Darragh's image which allows to use GPU
    `nvidia-docker run --ipc=host -v $PWD:/workspace/DeepFakeChallenge/ -v /data/DeepFakeDataProcessed:/workspace/DeepFakeChallenge/data_processed/ -v /data/DeepFakeData/unzip/:/workspace/DeepFakeChallenge/data/ -w=/workspace -p 8888:8888 --rm -it darraghdog/kaggle:deepfake4 jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/workspace/ --allow-root`


