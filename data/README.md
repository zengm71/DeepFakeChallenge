# Getting Data

## Sample Data Set
Please run `setup.sh` in the docker container, make sure to use your own Kaggle API key for password. 

## Full Data Set
I recommend doing this on a VM: even if your local machine has the storage, it is unlikely to have the power to process it. 

1. VSI

    Follow mostly the instructions from [week2/lab2](https://github.com/MIDS-scaling-up/v2/tree/master/week02/lab2):

    1.1 Request new instances 
        
        *  GPU
            Right now I'm doing this on a P100D

            `ibmcloud sl vs create --datacenter=wdc07 --hostname=kaggle-gpu --domain=W251-zengm71.cloud --image 3651552 --billing=hourly --network 1000 --key=1717878 --flavor AC1_8X60X25 --san`
        
        * CPU
            `ibmcloud sl vs create --datacenter=sjc03 --hostname=kaggle-cpu --cpu=4 --memory=32768 --domain=W251-zengm71.cloud --os=UBUNTU_16_64 --billing=hourly --san --disk=100 --network 1000  --key=1717878 --key=1545088`

    Note if you are using the GPU instance, you can skip ahead to `2. Mount COS Bucket`
    
    1.2 Harden VSI
        
    ```
    Edit /etc/ssh/sshd_config and make the following changes to prevent brute force attacks
    PermitRootLogin prohibit-password
    PasswordAuthentication no
    Restart the ssh daemon: service sshd restart
    ```

    3 Install docker:
        
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

    4 Mount disk:

    What is it called?    `fdisk -l`

    You should see your large disk, something like this
    ```
    Disk /dev/xvdc: 2 TiB, 2147483648000 bytes, 4194304000 sectors
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    In this case, our disk is called /dev/xvdc. Your disk may be named differently. Format it:
    ```
    
    ```
    # first
    mkdir -m 777 /data
    mkfs.ext4 /dev/xvdc
    ```
    Add to /etc/fstab

    ```
    # edit /etc/fstab and all this line:
    /dev/xvdc /data                   ext4    defaults,noatime        0 0
    ```
    Mount the disk    `mount /data`

    Move the working Docker directory
    By default, docker stores its images under /var/lib/docker , which will quickly fill up. So,
    ```
    service docker stop
    cd /var/lib
    cp -r docker /data
    rm -fr docker
    ln -s /data/docker ./docker
    service docker start
    ```
2. Mount COS Bucket

    The s3fs-fuse GitHub page has all the details on building and installing the package.
    ```
    sudo apt-get update
    sudo apt-get install automake autotools-dev g++ git libcurl4-openssl-dev libfuse-dev libssl-dev libxml2-dev make pkg-config
    git clone https://github.com/s3fs-fuse/s3fs-fuse.git
    ```
    Build and install the library
    ```
    cd s3fs-fuse
    ./autogen.sh
    ./configure
    make
    sudo make install

    You could also just apt install -y s3fs, but linux repos often have these tools backlevel, so..
    ```
    ```
    echo "f617796985ae40439fb04b99392dfb3e:a53f28551b913ccc4783ff88a4ce4bc2b72b0e655cbe5dc5" > $HOME/.cos_creds
    chmod 600 $HOME/.cos_creds
    ```
    Here use your own credential, since the bucket is public and you only need read access. 

   
    Create a directory where you can mount your bucket. Typically, this is done in the /mnt directory on Linux, notice the bucket is created in the IBM Cloud UI
    ```
    sudo mkdir -m 777 /data/DeepFakeData
    sudo s3fs dfdc-unzip /data/DeepFakeData -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-south.cloud-object-storage.appdomain.cloud
    ```
    ```
    sudo mkdir -m 777 /data/DeepFakeDataProcessed
    sudo s3fs dfdc-processed /data/DeepFakeDataProcessed -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-south.cloud-object-storage.appdomain.cloud
    ```
    Now you should see the mp4s in folder `/data/DeepFakeData/` in a few minutes. 

3. If you have to download the data, here is what you would do
    
    3.1 log into Kaggle.com and get your cookies on the site downloaded as `cookies.txt`. This is a very useful [plugin](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg/related?hl=en) for that
    
    3.2 place `cookies.txt` under /data/DeepFakeData
    
    3.3 Run the following command:
    ```
    sudo apt install aria2
    aria2c -c -x 16 -s 16 --load-cookies cookies.txt -p https://www.kaggle.com/c/16880/datadownload/dfdc_train_all.zip
    ```
    The process takes about an hour
    
    3.4 Unzip it `python3 unzip.py`, though you will have to tweak the code a bit to point it to the right directories. This process takes about an hour as well. 
