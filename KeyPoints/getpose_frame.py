import deeplabcut.pose_estimation_tensorflow.nnet as nn
import numpy as np
import tensorflow as tf
from deeplabcut.pose_estimation_tensorflow.config import load_config
from deeplabcut.pose_estimation_tensorflow.nnet import predict
import cv2
import os
from deeplabcut.utils import auxiliaryfunctions
from pathlib import Path
from skimage.util import img_as_ubyte
from deeplabcut.utils.auxfun_videos import imread
import deeplabcut.pose_estimation_tensorflow.util.visualize as vis
import csv
import glob
#the outputs of this script are predicted image "*_.t" and joint pose file "*.csv"
cur_path = "F:/BodyMeasurement/manuscript/gitee-code/"

#replace cur_path with your path
sides = "left_m"  #"left_m", "right_m", "top"
#chose side views

img_nums = 1;
#limit top img_nums to be processed

def getpose_frame(filename, config):
    vers = (tf.__version__).split(".")
    if int(vers[0]) == 1 and int(vers[1]) > 12:
        TF = tf.compat.v1
    else:
        TF = tf
    from deeplabcut.pose_estimation_tensorflow.nnet.net_factory import pose_net
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

    cfg = auxiliaryfunctions.read_config(config)

    trainFraction = cfg["TrainingFraction"][0]
    shuffle = 1 

    modelfolder = os.path.join(
        cfg["project_path"],
        str(
            auxiliaryfunctions.GetModelFolder(
                trainFraction, shuffle, cfg, modelprefix=""
            )
        ),
    )
    path_test_config = Path(modelfolder) / "test" / "pose_cfg.yaml"

    try:
        dlc_cfg = load_config(str(path_test_config))
    except FileNotFoundError:
        raise FileNotFoundError(
            "It seems the model for shuffle %s and trainFraction %s does not exist."
        )

    # if TFGPUinference:
    if "TF_CUDNN_USE_AUTOTUNE" in os.environ:
        del os.environ["TF_CUDNN_USE_AUTOTUNE"]  # was potentially set during training
    # if gputouse is not None:  # gpu selection
    #     os.environ["CUDA_VISIBLE_DEVICES"] = str(gputouse)
    try:
        Snapshots = np.array(
            [
                fn.split(".")[0]
                for fn in os.listdir(os.path.join(modelfolder, "train"))
                if "index" in fn
            ]
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "Snapshots not found! It seems the dataset for shuffle %s has not been trained/does not exist.\n Please train it before using it to analyze videos.\n Use the function 'train_network' to train the network for shuffle %s."
            % (shuffle, shuffle)
        )

    dlc_cfg["init_weights"] = os.path.join(
        modelfolder, "train", Snapshots[-1]
    )

    trainingsiterations = (dlc_cfg["init_weights"].split(os.sep)[-1]).split("-")[-1]


    #sess, inputs, outputs = predict.setup_GPUpose_prediction(dlc_cfg)
    # else:
    sess, inputs, outputs = predict.setup_pose_prediction(dlc_cfg)
    #image = cv2.imread("cow_screenshot2.png")

    #filename = '2.png'#"cow_screenshot.png"

    if filename == None:
        print("file not found")
        return

    image = imread(filename, mode="RGB")

    #---------------------------------------------------------------
    # Function: getposeNP() 
    # nx = image.shape[0]
    # ny = image.shape[1]
    #
    # frames = np.empty(
    #     (1, nx, ny, 3), dtype="ubyte"
    # )
    #
    # frames[0] = img_as_ubyte(image)
    #
    # pose = nn.predict.getposeNP(frames,dlc_cfg,sess,inputs,outputs)

    pose = nn.predict.getpose(image,dlc_cfg,sess,inputs,outputs)
    #print(pose)

    filter = True
    #filter pridected joint with score less than 0.1
    if filter:
        numjoint = pose.shape[0]
        for joint in range(numjoint):
            cur_score = pose[joint, 2]
            if cur_score < 0.01:
                pose[joint, 0] = 0
                pose[joint, 1] = 0

    #print(pose)

    img_labeled = vis.visualize_joints(image,pose)
    cv2.imwrite("labeled_" + filename,img_labeled)

    return pose

def vis_joints(img,output_filename,pose):
    image = vis.visualize_joints(img, pose)
    cv2.imwrite(output_filename, image)


if __name__ == "__main__":
    config= cur_path + "/KeyPoints/body_measurement-Du-2021-04-23/config.yaml"####"D:\DLC_sup\config.yaml"
    #config=r"F:/DLC_Cow/body_measurement-Du-2021-04-23/config.yaml"
    # list_ = []
    # list_erase = []
    ### number file name
    file_list = sorted(glob.glob(os.path.join(sides+"/","*.png")))
    print(os.getcwd())
    for i in range(img_nums):
    #     ###1 predict the images in folder test 
    #     filename = "test/pig_top/" + str(img) + ".png"

        ### glob file name
        filename = file_list[i-1]
        #for filename in file_list:
        pose = getpose_frame(filename, config)
        output_filename = filename.replace(".png","_t.png")
        print(output_filename)
        print(pose.shape)

        # draw joints on color/depth images
        color_img = cv2.imread(filename)
        vis_joints(color_img, output_filename, pose)
        #break

        #####2 test images without mark
        # filename = "F:/DLC_Cow/body_measurement-Du-2021-04-23/labeled-data/VID_65"
        # img_list = glob.glob(os.path.join(filename,"*.png"))
        # for img_name in img_list:
        #     pose = getpose_frame(img_name, config)
        #     output_filename = img_name.replace(".png","_t.png")
        #     color_img = cv2.imread(img_name)
        #     vis_joints(color_img, output_filename, pose)


        # ### wrire pose into csv file
        csv_filename = filename.replace(".png",".csv")
        with open(csv_filename,'w',newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerows(pose)


        ### mapping coordinates of joints to the depth image
        # numjoint = pose.shape[0]
        # for joint in range(numjoint):
        #     joint_x = pose[joint, 0]
        #     if joint_x != 0:
        #         pose[joint, 0] -= 90
        #         pose[joint, 1] += 20

        #print(pose)
        # save the picture with ploted joints
        # vis_filename = filename.replace("_s.png","_depth.png")
        # depth_img = cv2.imread(vis_filename)

        ## draw joints on color/depth images
        # color_img = cv2.imread(filename)
        # vis_joints(color_img, output_filename, pose)

        ### print the depth of joints
        # joint_depth=[]
        # for index in range(15):
        #     # joint_depth.append(int(pose[index][1]))
        #     # joint_depth.append(int(pose[index][0]))
        #     joint_depth.append(depth_img[int(pose[index][1])][int(pose[index][0])][0])
        # print(joint_depth)

        # for position in pose:
        #     position = np.delete(position,2)
        #     list_.append(position)
        # list_erase = [y for x in list_ for y in x]
        # print(len(list_erase))
        # list_.append(list_erase)
    #print(list_)
    