import os
import torch
import glob
import time
import numpy as np
import pandas as pd
import mmcv, cv2
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from IPython import display
from tqdm import tqdm
from matplotlib import pyplot as plt

Image.__version__
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

# Load face detector
mtcnn = MTCNN(margin=14, keep_all=True, post_process=False, thresholds = [0.9, 0.9, 0.9], device=device).eval()

# Load facial recognition model, but I didn't want to use it yet
resnet = InceptionResnetV1(pretrained='vggface2', device=device).eval()

class DetectionPipeline:
    """Pipeline class for detecting faces in the frames of a video file."""
    
    def __init__(self, detector, n_frames=None, batch_size=60, resize=None):
        """Constructor for DetectionPipeline class.
        
        Keyword Arguments:
            n_frames {int} -- Total number of frames to load. These will be evenly spaced
                throughout the video. If not specified (i.e., None), all frames will be loaded.
                (default: {None})
            batch_size {int} -- Batch size to use with MTCNN face detector. (default: {32})
            resize {float} -- Fraction by which to resize frames from original prior to face
                detection. A value less than 1 results in downsampling and a value greater than
                1 result in upsampling. (default: {None})
        """
        self.detector = detector
        self.n_frames = n_frames
        self.batch_size = batch_size
        self.resize = resize
    
    def __call__(self, filename):
        """Load frames from an MP4 video and detect faces.

        Arguments:
            filename {str} -- Path to video.
        """
        # Create video reader and find length
        v_cap = cv2.VideoCapture(filename)
        v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Pick 'n_frames' evenly spaced frames to sample
        if self.n_frames is None:
            sample = np.arange(1, v_len)
        else:
            sample = np.linspace(1, v_len - 1, self.n_frames).astype(int)

        # Loop through frames
        faces = []
        frames = []
        for j in range(v_len):
            success = v_cap.grab()
            if j in sample:
                # Load frame
                success, frame = v_cap.retrieve()
                if not success:
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                max_p = frame.max()
                frame = Image.fromarray(frame)
                if max_p < 150:
                    enhancer = ImageEnhance.Brightness(frame)
                    frame = enhancer.enhance(255/max_p)
                    
                # Resize frame to desired size
                if self.resize is not None:
                    frame = frame.resize([int(d * self.resize) for d in frame.size])
                
                frames.append(frame)

                # When batch is full, detect faces and reset frame list
                if len(frames) % self.batch_size == 0 or j == sample[-1]:
                    faces.extend(self.detector(frames))
                    frames = []

        v_cap.release()

        return faces    


def process_faces(faces, resnet):
    # Filter out frames without faces
    faces = [f for f in faces if f is not None]
    faces = torch.cat(faces).to(device)

    # Generate facial feature vectors using a pretrained model
    embeddings = resnet(faces)

    # Calculate centroid for video and distance of each face's feature vector from centroid
#     centroid = embeddings.mean(dim=0)
#     x = (embeddings - centroid).norm(dim=1).cpu().numpy()
    
    return embeddings

# Define face detection pipeline
detection_pipeline = DetectionPipeline(detector=mtcnn, batch_size=60, resize=None, n_frames=45)
start = time.time()
n_processed = 0
with torch.no_grad():
    for f in tqdm(np.arange(0, 50, 2), total = len(np.arange(0, 50, 2))):
        # Get all videos
        filenames = glob.glob('data/dfdc_train_part_' + str(f) + '/*.mp4')
        metadata = pd.read_json('data/dfdc_train_part_' + str(f) + '/metadata.json').T
        print('data/dfdc_train_part_' + str(f) + '/*.mp4 | '+ str(len(filenames)) + ' files')
        X1 = []
        X1_encoded = []
        Y1 = []
        X2 = []
        X2_encoded = []
        Y2 = []
        X3 = []
        X3_encoded = []
        Y3 = []
        start = time.time()
        n_processed = 0
        for i, filename in tqdm(enumerate(filenames), total= len(filenames)):
            try:
                # Load frames and find faces
                faces = detection_pipeline(filename)
                y = int((metadata.label['data/dfdc_train_part_' + str(f) + '/' + metadata.index == filename] == 'REAL') * 1)
                n_faces = [x.shape[0] if x is not None else 0 for x in faces ]
                faces = [x for x in faces if x is not None]
                if n_faces.count(3) >= 30:
                    f_faces = [x for x in faces if x.shape[0] == 3]
                    f_faces = [f_faces[i] for i in np.linspace(0, len(f_faces)-1, 30).astype(int)]
                    X3.append(torch.cat(f_faces))
                    X3_encoded.append(process_faces(f_faces, resnet))
                    Y3.append(y)
                elif n_faces.count(2) >= 30:
                    f_faces = [x for x in faces if x.shape[0] == 2]
                    f_faces = [f_faces[i] for i in np.linspace(0, len(f_faces)-1, 30).astype(int)]
                    X2.append(torch.cat(f_faces))
                    X2_encoded.append(process_faces(f_faces, resnet))
                    Y2.append(y)
                elif n_faces.count(1) >= 30:
                    f_faces = [x for x in faces if x.shape[0] == 1]
                    f_faces = [f_faces[i] for i in np.linspace(0, len(f_faces)-1, 30).astype(int)]
                    X1.append(torch.cat(f_faces))
                    X1_encoded.append(process_faces(f_faces, resnet))
                    Y1.append(y)
            except KeyboardInterrupt:
                print('\nStopped.')
                break

            except Exception as e:
                print(e)

        n_processed += len(faces)
        print(f'Frames per second (load+detect+embed): {n_processed / (time.time() - start):6.3}\r', end='')
        torch.save(X1_encoded, 'data_processed/1face_X_part' + str(f) + '.pt')
        torch.save(Y1, 'data_processed/1face_Y_part' + str(f) + '.pt')
        torch.save(X2_encoded, 'data_processed/2face_X_part' + str(f) + '.pt')
        torch.save(Y2, 'data_processed/2face_Y_part' + str(f) + '.pt')
        torch.save(X3_encoded, 'data_processed/3face_X_part' + str(f) + '.pt')
        torch.save(Y3, 'data_processed/3face_Y_part' + str(f) + '.pt')