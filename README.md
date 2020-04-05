# DeepFakeChallenge

## Setup

1. Provision a p100 virtual server on ibmcloud(preferrably).

2. `ssh` into your p100 virtual server and clone this repository

    `git clone https://github.com/zengm71/DeepFakeChallenge.git`

2. Run `docker_setup.sh` script to install CUDA 10.0, docker, and nvidia-docker on your p100 virtual server.

    NOTE: Just press 'y' if the script shows any prompt

3. Prepare the secondary disk

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

4. Mount COS Bucket

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
    sudo mkdir -m 777 /data/DeepFakeDataProcessed
    sudo s3fs dfdc-processed /data/DeepFakeDataProcessed -o passwd_file=$HOME/.cos_creds -o sigv2 -o use_path_request_style -o url=https://s3.us-south.cloud-object-storage.appdomain.cloud
    ```
    Now you should see the mp4s in folder `/data/DeepFakeData/` in a few minutes
    

5. Copy the processed images from `/data` to `/DeepFakeChallenge/data_processed`

    `cp -a /data/DeepFakeDataProcessed/. data_processed`

6. Run the docker code below to start a jupyter notebook!

    `nvidia-docker run --ipc=host -v $PWD:/workspace/DeepFakeChallenge/ -v /data/DeepFakeDataProcessed:/workspace/DeepFakeChallenge/data_processed/ -v /data/DeepFakeData/unzip/:/workspace/DeepFakeChallenge/data/ -w=/workspace -p 8888:8888 --rm -it darraghdog/kaggle:deepfake4 jupyter notebook --no-browser --ip="0.0.0.0" --notebook-dir=/workspace/ --allow-root`

