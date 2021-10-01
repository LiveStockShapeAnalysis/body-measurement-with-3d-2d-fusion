#usr/bin/env python
#-*- coding: utf-8 -*-

import win32api
import win32event
import win32process

cur_path = "F:/BodyMeasurement/manuscript/gitee-code/"

#exe usage:argv[0]: .exe   argv[1]:left point cloud    argv[2] : left keypoints.csv    argv[3] : left_matrix
#           argv[4]:right point cloud   argv[5] : right keypoints.csv   argv[6] : right_matrix
#           argv[7]:top point cloud   argv[8] : top keypoints.csv   argv[9]: left girth points
#           argv[10]:right girth points    argv[11]:left illum points   argv[12]:right illum points
#           argv[13]:left oblique points   argv[14]:right oblique points   argv[15]: Matrix_pose_normalization

def main():
    exePath = cur_path + "keypoint_measure.exe"
    ply_mx_path = cur_path + "PointCloud/"
    csvpath = cur_path + "KeyPoints/"
    test_name = "sample"
    for i in range(1):
        paramply_left = ply_mx_path+'LeftDepth/'+test_name+"_.pcd"
        paramply_right = ply_mx_path+'RightDepth/'+test_name+"_.pcd"
        paramply_top = ply_mx_path + 'TopClouds/' +test_name+"_.pcd"
        paramcsv_left = csvpath+'left_m/'+test_name+"_3d.csv"
        paramcsv_right = csvpath+'right_m/'+test_name+"_3d.csv"
        paramcsv_top = csvpath+'top/'+test_name+"_3d.csv"
        paramcsv_gl = csvpath+'left_m/'+test_name+"_3d_g.csv"
        paramcsv_gr = csvpath+'right_m/'+test_name+"_3d_g.csv"
        paramcsv_ob_l = csvpath+'left_m/'+test_name+"_3d_o.csv"
        paramcsv_ob_r = csvpath+'right_m/'+test_name+"_3d_o.csv"
        paramcsv_iw_l = csvpath+'left_m/'+test_name+"_3d_iw.csv"
        paramcsv_iw_r = csvpath+'right_m/'+test_name+"_3d_iw.csv"

        Matrix_left = ply_mx_path + 'matrices_txt/' + test_name +'_l.txt'
        Matrix_right = ply_mx_path + 'matrices_txt/' + test_name + '_r.txt'
        Matrix_normalization = ply_mx_path + 'TopClouds/'+test_name+"_3d.txt"
        
        param = (paramply_left + " " + paramcsv_left + " " + Matrix_left + " " 
            + paramply_right + " " + paramcsv_right + " " + Matrix_right + " " 
            + paramply_top + " " + paramcsv_top +" "+paramcsv_gl+" "
            +paramcsv_gr+" "+paramcsv_ob_l+" "+paramcsv_ob_r+" "
            +paramcsv_iw_l+" "+paramcsv_iw_r+ " " + Matrix_normalization)

        win32api.ShellExecute(0,
                            "open",
                            exePath,
                            param,
                            '',
                            1)
if '__main__' == __name__:
    main()