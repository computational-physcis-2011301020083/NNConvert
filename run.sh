path1="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0317/DataVRGhost/Hbb/301497.hbbTraining.e3820_s3126_r9364_p3990.2019_pub.hbbTag_v1_H.20672786._000001.output.h5"
path2="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0317/DataVRGhost/Top/301332.hbbTraining.e4061_s3126_r9364_p3990.2019_pub.hbbTag_v1_T.20672769._000001.output.h5"
path3="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0317/DataVRGhost/Dijets/361031.hbbTraining.e3569_s3126_r9364_p3990.2019_pub.hbbTag_v1_N.20672831._000005.output.h5"

python predict.py --path $path1
python predict.py --path $path2 
python predict.py --path $path3  


