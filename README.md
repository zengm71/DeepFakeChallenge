# DeepFakeChallenge

# Setup
## VSI
### GPU
Right now I'm doing this on a P100D

`ibmcloud sl vs create --datacenter=wdc07 --hostname=kaggle-gpu --domain=W251-zengm71.cloud --image 3651552 --billing=hourly --network 1000 --key=1717878 --flavor AC1_8X60X25 --san`
### CPU
`ibmcloud sl vs create --datacenter=sjc03 --hostname=kaggle-cpu --cpu=4 --memory=32768 --domain=W251-zengm71.cloud --os=UBUNTU_16_64 --billing=hourly --san --disk=100 --network 1000  --key=1717878 --key=1545088`
* Harden VSI
    ```
    Edit /etc/ssh/sshd_config and make the following changes to prevent brute force attacks
    PermitRootLogin prohibit-password
    PasswordAuthentication no
    Restart the ssh daemon: service sshd restart
    ```
* Install docker:
    ```
    # Validate these at https://docs.docker.com/install/linux/docker-ce/ubuntu/
    apt-get update
    apt install apt-transport-https ca-certificates 
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic test" 
    apt update 
    apt install docker-ce
    # Validated 09/14/19 - Darragh
    # Test if docker hello world is working
    docker run hello-world
    ```
## Docker 
    I used Darragh's image which allows to use GPU
    `nvidia-docker run --ipc=host -v $PWD:/workspace/DeepFakeChallenge/ -w=/workspace -p 8888:8888 --rm -it darraghdog/kaggle:deepfake4 jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/workspace/ --allow-root`
