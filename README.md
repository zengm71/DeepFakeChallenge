# DeepFakeChallenge

# Setup
## VSI
    Right now I'm doing this on a P100D
    `ibmcloud sl vs create --datacenter=wdc07 --hostname=p100 --domain=W251-zengm71.cloud --image 3651552 --billing=hourly --network 1000 --key=1717878 --flavor AC1_8X60X25 --san`
## Docker 
    I used Darragh's image which allows to use GPU
    `nvidia-docker run --ipc=host -v $PWD:/workspace/DeepFakeChallenge/ -w=/workspace -p 8888:8888 --rm -it darraghdog/kaggle:deepfake4 jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/workspace/ --allow-root`
