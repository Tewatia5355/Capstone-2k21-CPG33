import pandas as pd
import numpy as np
import librosa
import glob, os
from sklearn.model_selection import train_test_split
from keras.layers import Convolution1D, MaxPooling2D
from keras.layers.convolutional import Conv1D, Conv2D
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution1D, MaxPooling1D
from tensorflow.keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
import tensorflow as tf
import tensorflow.keras
import keras
from keras import optimizers
from boruta import BorutaPy

Label_chk = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]


def find_emotion(path):
    model1 = Sequential()
    model1.add(Conv1D(32, 3, padding="same", input_shape=(x_train.shape[1], 1)))  # 1
    model1.add(Activation("relu"))
    model1.add(Conv1D(64, 3, padding="same"))  # 2
    model1.add(Activation("relu"))
    model1.add(Dropout(0.25))
    model1.add(MaxPooling1D(pool_size=(2)))
    model1.add(Conv1D(64, 3, padding="same"))  # 3
    model1.add(Activation("relu"))
    model1.add(Dropout(0.25))
    model1.add(Conv1D(16, 3, padding="same"))  # 4
    model1.add(Activation("relu"))
    model1.add(Flatten())
    model1.add(Dense(7))  # 5
    model1.add(Activation("softmax"))
    opt = tf.keras.optimizers.RMSprop(learning_rate=0.00001, decay=1e-6)

    # here kaiser_fast is a technique used for faster extraction
    X, sample_rate = librosa.load(path, res_type="kaiser_fast", sr=16000)
    # we extract mfcc feature from data
    mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
    delta_m = librosa.feature.delta(mfccs)
    delta2_m = librosa.feature.delta(mfccs, order=2)
    feature = []
    for k in mfccs:
        feature.append(k)
    for k in delta_m:
        feature.append(k)
    for k in delta2_m:
        feature.append(k)
    feature = feat_selector.transform((pd.DataFrame(feature).to_numpy()).transpose())
    part = path2.split(".")[0].split("_")
    label = "".join([x for x in part[2] if not x.isdigit()])
    df2 = [feature, label]

    model1.load_weights("best_model.hdf5")

    tt = model1.predict(df2[0])
    classes_x = np.argmax(tt, axis=1)

    return Label_chk[classes_x[0]]
