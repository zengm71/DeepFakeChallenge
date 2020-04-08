# DeepFakeChallenge
### W251 Deep Learning in the Cloud and at the Edge (Spring 2020) Final Project

## Abstract

* Participate in the Deepfake Detection Challenge (Kaggle)
* Predict whether or not a particular video is a deep fake
* Use IBM Cloud for pipeline
* Report findings/results

## Introduction

Deepfake techniques enable a realistic AI-generated videos of people doing and saying fictional things. This technology lies within the field of computer vision, a subfield of computer science, and we have seen similar crude methods of photo manipulation (a.k.a, "photoshopping") before that somehow resembles the end results of Deepfakes. The term "deepfakes" was believed to be originated around the end of 2017 in a Reddit community r/deepfakes by a Reddit user named "deepfakes". Perhaps an example below would ring a bell.

![Cage_Adams](images/Deepfake_example.gif)

By Source (WP:NFCC#4), Fair use, https://en.wikipedia.org/w/index.php?curid=61555724

Popularized by the various swaps of Nicholas Cage's face, the technology makes its mainstream debut in January 2018 as a proprietary desktop application called "FakeApp", which then gets superseded by Faceswap. The rising interest in DeepFake was not only supported by the amateur/commercial development efforts, but also supported by the academic institutions as a group of reserachers from University of California, Berkeley have published a paper in August 2018 that expands the application of deepfakes to an entire body. 

Initial reactions to Deepfake techniques have been worriesome as these realistic fake videos have the potential to significantly impact how people determine the legitimacy of information presented online. As a result, AWS, Facebook, Microsoft, the Partnership on AI's Media Integrity Steering Committee, and academics have collaborated to launch a DeepFake Detection Challenge (DFDC) on Kaggle, in order to promote collaboration and contribute to an effort to build a robust response to the emerging threat of Deepfakes. 

## Dataset

There were 4 datasets available from the DeepFake Deep Challenge on Kaggle. Among those 4 datasets, we used the Training Set to train our neural net and used the Public Validation Set to evaluate our models before submission. 

* *Training Set* - Originally broken up in 50 zipped files (471.84 GB) that can be accessed through GCS bucket after accepting the competition rules. 

* *Public Validation Set* - There are 400 vidoes/ids in this dataset. The submission file output for the Kaggle competition will be based on this dataset. 

The data is comprised of .mp4 files, split into compressed sets of ~10GB apiece. Along with the videos, there is a metadata.json file that lists the `filename` for the videos, `label`(REAL/FAKE), `original` (filename of the original video, if the video is fake), `split` (will always be "train").

### EDA

Adam's stuff?


## Pipeline

* 2 p100s were used to process the videos from the training set (CUDA 10.0 ENV)

    * MTCNN was used for face detection
        `mtcnn = MTCNN(margin=14, keep_all=True, post_process=False, thresholds = [0.9, 0.9, 0.9], device=device).eval()`

    * pre-trained weights from the resnet 'vggface2' was loaded to generate 1D facial feature vectors
        `resnet = InceptionResnetV1(pretrained='vggface2', device=device).eval()`
        
    * We took 30 frames from each video
    
    * Processing Time: From the unit testing of our pipeline, we were able to see that processing of 400 videos took about 18 minutes on a pair of P100s, which was about 22 videos per minute. Assuming that there are around 2,000 videos per folder and knowing the fact that there are 50 folders, we can expect this process to take about 100,000 / 22 = ~4,500 minutes, which translates to about 75 hours. 
    
    

## Model Architecture

* LSTM 

## Evaluation

<img src="https://render.githubusercontent.com/render/math?math=\textrm{LogLoss} = - \frac{1}{n} \sum_{i=1}^n \left[ y_i \log(\hat{y}_i) + (1 - y_i) \log(1 - \hat{y}_i)\right]">

The use of log provides extreme punishments for being both confident and wrong. 

## Conclusion

## References