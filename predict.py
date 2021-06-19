import argparse
import os,glob,h5py,ROOT,shutil
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--model", dest='model',  default="", help="model")
args = parser.parse_args()
import tensorflow as tf
from keras import backend as K
import keras
from keras.models import Model, Sequential
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

#Read the dataset
features1=['mcEventWeight','eventNumber','mass','pt','eta'] #0-9
features2=['DL1rT_pu', 'DL1rT_pc', 'DL1rT_pb', 'relativeDeltaRToVRJet']
list3={}
list4={}
list5={}
for i in features2:
      list3[i]=i+"_1"
      list4[i]=i+"_2"
      list5[i]=i+"_3"
paths=args.path
h0=pd.read_hdf(paths,"fat_jet")[features1]
h1=pd.read_hdf(paths,"subjet_VRGhostTag_1")[features2]
h1.rename(columns=list3,inplace=True)
h2=pd.read_hdf(paths,"subjet_VRGhostTag_2")[features2]
h2.rename(columns=list4,inplace=True)
h3=pd.read_hdf(paths,"subjet_VRGhostTag_3")[features2]
h3.rename(columns=list5,inplace=True)
h=pd.concat([h0,h1,h2,h3], axis=1)
h["dsid"]=1 #int(paths.split(".")[2])
#Pt in GeV
h["pt"] = (h["pt"]/1000.0).astype("float64")
h["mass"] = (h["mass"]/1000.0).astype("float64")
Data=h[['mcEventWeight','relativeDeltaRToVRJet_1','relativeDeltaRToVRJet_2','relativeDeltaRToVRJet_3','eventNumber','dsid','mass','pt','eta','DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1','DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2','DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3']]
Data=Data.values

#Normalize the data
Data=Data[Data[:,7]<3000.]
train=Data[:,7:18]
meanFile=h5py.File("meanstd.h5","r")
mean_vector=meanFile.get("mean")
std_vector=meanFile.get("std")
train=(train-mean_vector[:,0:11])/std_vector[:,0:11]
train=np.nan_to_num(train)

#Prepare the inputs
fatjet=train[:,0:2] # 'pt','eta'
subjet0=train[:,2:5] # 'DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1'
subjet1=train[:,5:8] # 'DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2'
subjet2=train[:,8:11] # 'DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3'

#Feeds it to Keras to call predict
#4 inputs for the model JKDL1r: fatjet('pt','eta'), subjet0('DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1'), subjet1('DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2'), subjet2('DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3')
JKDL1r="WeiAdmStd_JKDL1r.h5"
JKDL1r_pre = keras.models.load_model(JKDL1r)
JKDL1r_data=[fatjet,subjet0,subjet1,subjet2]
predictions_JKDL1r=JKDL1r_pre.predict(JKDL1r_data)
print predictions_JKDL1r[110:130,:]



