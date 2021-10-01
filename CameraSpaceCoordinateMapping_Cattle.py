#usr/bin/env python
#-*- coding: utf-8 -*-

import win32api
import win32event
import win32process
import os
import glob

cur_path = "F:/BodyMeasurement/manuscript/gitee-code/"
sides = "left_m" #left_m,right_m,top
depth_side = "LeftDepth" #LeftDepth,RightDepth,TopClouds

def main():
    exePath = cur_path + "KeyPoints/CoordinateMapper.exe"
    csv_path = cur_path + "KeyPoints/" + sides + "/sample.csv"
    depth_path = cur_path + "PointCloud/" + depth_side + "/sample.png"
 
    para = csv_path + " " + depth_path

    win32api.ShellExecute(0,
                        "open",
                        exePath,
                        para,
                        '',
                        1)
if '__main__' == __name__:
    main()  