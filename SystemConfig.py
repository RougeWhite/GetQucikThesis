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
@FileName  :SystemConfig.py

@Time      :2022/8/2 17:35

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :
'''
import sys
import os
import json

class SystemConfig:

    def Setting(self,retval, default_setting_filename):

        default_setting_filename_dir = retval + "\\" + default_setting_filename
        if os.path.exists(default_setting_filename_dir):
            # 读取配置文件
            SetJson = self.loadSet(default_setting_filename_dir)
            User_Setting_filename = SetJson["userconfig"]
            User_setting_filename_dir = retval + "\\" + User_Setting_filename
            #  创建配置文件
            if os.path.exists(User_setting_filename_dir) ^ 1:
                print("正在创建配置文件,请稍后")
                self.text_create(User_setting_filename_dir,'你好')
                print("用户配置文件创建完成")
                return SetJson
            else:
                print("用户配置文件存在")
                return SetJson
        else:
            print("code:400 初始化失败:配置文件丢失")
            sys.exit()
    # 加载系统设置
    def loadSet(self,default_setting_filename_dir):
        with open(default_setting_filename_dir, 'r', encoding='utf-8') as f:
            SetJson = json.load(f)
        return SetJson

    # 新建文件
    def text_create(self,path, msg):
        f = open(path, 'w', encoding='utf-8')
        f.write(msg)
        f.close()

    # 获取用户设置
    def GetUserSet(self,SetJson):
        Now_Path = os.getcwd()
        UserSetFileName = SetJson["userconfig"]
        Dir_Name = Now_Path + "\\" + UserSetFileName
        f = open(Dir_Name)
        data = f.readlines()
        return data