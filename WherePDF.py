# -*- coding:utf-8 -*-
#                 ____                                       _____  __         
#                /\  _`\                                    /\___ \/\ \        
#                \ \ \L\_\  __  __     __      ___          \/__/\ \ \ \___    
#                 \ \ \L_L /\ \/\ \  /'__`\  /' _ `\           _\ \ \ \  _ `\  
#                  \ \ \/, \ \ \_\ \/\ \L\.\_/\ \/\ \         /\ \_\ \ \ \ \ \ 
#                   \ \____/\ \____/\ \__/.\_\ \_\ \_\        \ \____/\ \_\ \_\
#                    \/___/  \/___/  \/__/\/_/\/_/\/_/  _______\/___/  \/_/\/_/
#                                                      /\______\               
#                                                      \/______/  
'''
@FileName  :WherePDF.py

@Time      :2022/8/2 21:18

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :
'''

import os
import shutil
from glob import glob
from tkinter import *
import hashlib
import time
import re
import Gol



class movePDF:
    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time
    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        log_data_Text = Gol.get_value("log_data_Text")
        LOG_LINE_NUM = Gol.get_value("LOG_LINE_NUM")
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            log_data_Text.insert("end", logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
            Gol.set_value("LOG_LINE_NUM", LOG_LINE_NUM)
        else:
            log_data_Text.delete(1.0, 2.0)
            log_data_Text.insert("end", logmsg_in)


    def text_create(self,path):
        f = open(path, 'w', encoding='utf-8')
        f.close()

    def GetPDF2Data(self,SetJson):
        PDF_Path = SetJson["zotero_path"]
        New_Path_Input = SetJson["output_path"]

        FindTrue = False
        # PDF_Path = "E:\zotero\storage"    # 需要转移的PDF路径
        New_Path = New_Path_Input+"\\"
        # New_Path = "E:\\OneDrive\\论文\\PDFfromOther\\"    # 转移后的路径
        Toc_Name = SetJson["toc_name"]
        Dir_Name = New_Path + Toc_Name   # 目录配置名称

    #     判断目录文件是否存在
        if os.path.exists(Dir_Name) ^ 1:
            print("正在创建配置文件,请稍后")
            self.text_create(Dir_Name)

    #     获取路径下全部pdf文件
        for root, dirs, files in os.walk(PDF_Path):
            for File_Name in files:
                File_Name_List = File_Name.split(".")
                File_Name_Suffix = File_Name_List[len(File_Name_List)-1]
                if File_Name_Suffix == "pdf":
                    PDF_File_Path = os.path.join(root, File_Name)
                    # print(os.path.join(root, File_Name))
                    PDF_NAME = os.path.basename(PDF_File_Path)   # PDF名称
                    # print(PDF_NAME)
                    PDF_TIME = time.strftime("%Y-%m-%d", time.localtime(os.stat(PDF_File_Path).st_mtime))  # PDF 生成日期
                #   获取目录内的数据，并判断是否存在
                    f = open(Dir_Name,encoding="utf-8")
                    lines = f.read()
                    line_list = lines.split(",")
                    tmp_a = 0
                    for i in line_list:
                        if i == "\n" + PDF_NAME:
                            # self.write_log_to_Text("PDF文件已存在\n"+PDF_NAME)
                            FindTrue = False
                            break
                        else:
                            tmp_a = tmp_a + 1
                            if len(line_list) == tmp_a:
                                f = open(Dir_Name, "a",encoding="utf-8")
                                # 写入配置名称
                                f.write("\n" + PDF_NAME + ",")
                                print(PDF_NAME+"文件新增")
                                self.write_log_to_Text(PDF_NAME+"文件新增")
                                FindTrue = True
                                # 复制文件
                                src_file_list = glob(PDF_File_Path + PDF_NAME)  # glob获得路径下所有文件，可根据需要修改
                                for srcfile in src_file_list:
                                    self.mycopyfile(srcfile, New_Path)
                                break
                    f.close()
        return FindTrue, PDF_NAME

    def mycopyfile(self,srcfile, dstpath):  # 复制函数
        if not os.path.isfile(srcfile):
            print("%s not exist!" % (srcfile))
        else:
            fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)  # 创建路径
            shutil.copy(srcfile, dstpath + fname)  # 复制文件
            # self.write_log_to_Text("复制文件\n %s \n到\n %s" % (srcfile, dstpath + fname))
