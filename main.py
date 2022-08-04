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
@FileName  :main.py

@Time      :2022/8/2 17:34

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :
'''
import os
import webbrowser

import SystemConfig
import Gui
from tkinter import *
import time
import re
import os
import json
import GetData
import Gol
from threading import Thread
import base64


LOG_LINE_NUM = 0

class GUI():

    def __init__(self,init_window_name,SetJson):
        self.init_window_name = init_window_name
        self.SetJson = SetJson

    #设置窗口
    def set_init_window(self):
        SetJson = self.SetJson
        self.init_window_name.title("文献自动加载工具 v1.0 作者：Guan_Jh")           #窗口名
        self.init_window_name.geometry(str(SetJson['windows_width'])+'x'+str(SetJson['windows_height'])+'+'+str(SetJson['postion_x'])+'+'+str(SetJson['postion_y']))
        # 文献目录
        self.thesis_data_label = Label(self.init_window_name, text="文献目录txt位置：例如 E:\\thesis.txt")
        self.thesis_data_label.place(x=10,y=10)
        self.thesis_data_Text = Text(self.init_window_name, width=50, height=1)  # 原始数据录入框
        self.thesis_data_Text.insert(1.0, SetJson['txt_path'])
        self.thesis_data_Text.place(x=10,y=30)

        self.init_data_label = Label(self.init_window_name, text="Zotero文件位置：例如 E:\zotero\storage")
        self.init_data_label.place(x=10,y=50)
        self.init_data_Text = Text(self.init_window_name, width=50, height=1)  # 原始数据录入框
        self.init_data_Text.insert(1.0, SetJson['zotero_path'])
        self.init_data_Text.place(x=10,y=70)

        self.result_data_label = Label(self.init_window_name, text="聚集位置：例如 E:\OneDrive\论文\PDFfromOther")
        self.result_data_label.place(x=10,y=90)
        self.result_data_Text = Text(self.init_window_name, width=50, height=1)  #处理结果展示
        self.result_data_Text.insert(1.0, SetJson['output_path'])
        self.result_data_Text.place(x=10,y=110)

        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="开始搜寻", bg="lightblue", width=10,command=self.chick)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.place(x=130,y=140)

        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.place(x=10,y=180)
        self.log_data_Text = Text(self.init_window_name, width=50, height=14)  # 日志框
        self.log_data_Text.place(x=10,y=205)

        Gol.set_value("log_data_Text",self.log_data_Text)






    def chick(self):
        SetJson = self.SetJson
        PDF_Path_Input = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        thesis_Path_Input = self.thesis_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        New_Path_Input = self.result_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        PDF_Path = PDF_Path_Input.decode()
        New_Path = New_Path_Input.decode()
        thesis_Path = thesis_Path_Input.decode()
        # print(New_Path)
        PDF_Path_Vaild = re.search('.*:\\.*', PDF_Path)
        New_Path_Vaild = re.search('.*:\\.*', New_Path)
        thesis_Path_Vaild = re.search('.*\.txt', thesis_Path)
        if PDF_Path_Vaild and New_Path_Vaild and thesis_Path_Vaild and os.path.exists(thesis_Path):
            self.write_log_to_Text("输入路径有效，程序正在运行！")
            self.RunData()
        else:
            self.write_log_to_Text("输入有误，请重新输入")



    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        Gol.get_value("LOG_LINE_NUM")
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
            Gol.set_value("LOG_LINE_NUM", LOG_LINE_NUM)
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)

    def RunData(self):
        # 打开浏览器开始获取thesis_list_url
        t1 = Thread(target=self.dataGET)
        # 打开系统托盘
        t1.daemon = True
        t1.start()
    def dataGET(self):
        self.write_log_to_Text("请勿关闭！请勿重复点击按钮！")
        SetJson = self.SetJson
        ReadFile = GetData.ReadFile()
        Pdf_Deal = GetData.Pdf_Deal()
        # 读取需要获取的论文txt文件
        Thesis = ReadFile.GetThesisData(SetJson['txt_path'])
        thesis_list, url_list = ReadFile.AnsisyThesis(Thesis)
        thesis_list_url = Pdf_Deal.GetThesisList(thesis_list, SetJson)
        Gol.set_value("thesis_list",thesis_list)
        Gol.set_value("thesis_list_url",thesis_list_url)

        num = 0
        theFool = True
        for i in thesis_list_url:
            if i==[]:
                num = num+1
            if num == len(thesis_list_url):
                theFool = False
                self.write_log_to_Text("请更换代理并且输入如下网址完成人机验证\n"
                                       "https://scholar.google.com.hk/scholar?q=test")
                webbrowser.open("https://scholar.google.com.hk/scholar?q="+thesis_list[0])

        if thesis_list_url and theFool:
            self.write_log_to_Text("文献链接已找到，数目"+str(len(thesis_list_url))+"大约花费时间"+str((SetJson['wait_web']+SetJson['wait_pdf'])*len(thesis_list_url)))
            # 打开浏览器开始获取thesis_list_url
            t1 = Thread(target=self.GETpdf)
            # 打开系统托盘
            t1.daemon = True
            t1.start()

    def GETpdf(self):
        Pdf_Deal = GetData.Pdf_Deal()
        SetJson = self.SetJson
        thesis_list = Gol.get_value("thesis_list")
        thesis_list_url = Gol.get_value("thesis_list_url")
        Pdf_Deal.GetThesisPDF(thesis_list, thesis_list_url, SetJson)

global FindTrue


def openUI():
    SetJson = Gol.get_value("SetJson")

    init_window = Tk()
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode('AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAMQOAADEDgAAAAAAAAAAAAAAAAAAAAAAAHpGJf96RiX/ekYl/3pGJf96RiX/ekYl/3pGJf96RiX/ekYl/3pGJf96RiX/ekYl/wAAAAAAAAAAAAAAAAAAAAB6RiX/NDjj/zU55f81OeX/NTnl/zU55f81OeX/NTnl/zU55f81OeX/NDjk/3pGJf8AAAAAAAAAAAAAAAAAAAAAekYl/zU55f81OeX/NTnl/zU55f81OeX/NTnl/zU55f81OeX/NTnl/zU55f96RiX/AAAAAAAAAAAAAAAAAAAAADIy0/81OeX/NTnl/zU55f81OeX/ekYl/3pGJf81OeX/NTnl/zU55f81OeX/NDLN/wAAAAAAAAAAAAAAAAAAAAAvL9P/NTnl/4CK//+Aiv//NTnl/zU55f81OeX/NTnl/4CK//+Aiv//NTnl/y8v0/8AAAAAAAAAAAAAAAB6RiX/Ly/T/zU55f81OeX/YkJn/11Ad/81OeX/NTnl/2JCZ/9dQHf/NTnl/zU55f8vL9P/ekYl/wAAAAAAAAAAekYl/y8v0/81OeX/NTnl/zU55f81OeX/NTnl/zU55f81OeX/NTnl/zU55f81OeX/Ly/T/3pGJf8AAAAAAAAAAHpGJf8vL9P/NTnl/zU55f81OeX/NTnl/zU55f81OeX/NTnl/zU55f81OeX/NTnl/y8v0/96RiX/AAAAAAAAAAB6RiX/Ly/T/zU55f81OeX/Gr72/xq+9v8avvb/Gr72/xq+9v8avvb/NTnl/zU55f8vL9P/ekYl/wAAAAAAAAAAekYl/zEy2f9IzPj/Gr72/xq+9v8avvb/MsX2/xq+9v8avvb/Gr72/xq+9v8avvb/MTPZ/3pGJf8AAAAAAAAAAHpGJf8WqPX/U874/xq+9v8avvb/Gr72/1PO+P8avvb/JsH3/xq+9v8avvb/Gr72/1PO+P96RiX/AAAAAAAAAAB3Siz/U874/1PO+P8avvb/U874/xq+9v9Byfj/Gr72/1PO+P9Tzvj/Gr72/xq+9v9Tzvj/d0os/wAAAAB6RiX/Fqj1/1PO+P9Tzvj/Fqj1/1PO+P8avvb/U874/0TE9/9Tzvj/U874/xq+9v9Tzvj/U874/xao9f96RiX/ekUlYHpGJf9Tzvj/U874/1PO+P9Tzvj/U874/1PO+P9Myfj/U874/xmp9P8jsPX/U874/1PO+P96RiX/e0UkVQAAAAAAAAAAekYl/xao9f8WqPX/Fqj1/xao9f80i7b/Fqj1/xao9f8WqPX/ekYl/2ZZTv96RiX/AAAAAAAAAAAAAAAAAAAAAAAAAAB6RiXeekYl/3pGJf96RiX/AAAAAHdEIh56RiX/ekYl/3xGJyEAAAAAAAAAAAAAAAAAAAAAwAMAAMADAADAAwAAwAMAAMADAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAAAAAAIABAADAAwAA8Z8AAA=='))
    tmp.close()
    init_window.iconbitmap("tmp.ico")
    os.remove("tmp.ico")

    windowsgui = GUI(init_window,SetJson)
    windowsgui.set_init_window()
    init_window.mainloop()

if __name__ == '__main__':


    # 全局变量生效
    Gol._init()

    #  系统初始化
    systemconfig = SystemConfig.SystemConfig()
    Now_Path = os.getcwd()
    default_setting_filename = "config.json"
    default_setting_filename_dir = Now_Path + "\\" + default_setting_filename
    # # 打开系统托盘
    # app = MyApp()

    #  Setting
    # 获取系统设置
    SetJson = systemconfig.Setting(Now_Path, default_setting_filename)
    Gol.set_value("SetJson",SetJson)

    # 获取用户设置
    # UserSet = json.loads(str(systemconfig.GetUserSet(SetJson)).split('\'')[1])
    UserSet = systemconfig.GetUserSet(SetJson)
    Gol.set_value("UserSet", UserSet)
    openUI()

    # 设置根窗口默认属性

