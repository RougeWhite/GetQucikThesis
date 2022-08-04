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
@FileName  :GetData.py

@Time      :2022/8/2 17:51

@Author    :Guan_jh

@Email     :guan_jh@qq.com

@Describe  :
'''

import re
import os
import urllib.request as request
import requests
from bs4 import BeautifulSoup
import time
import webbrowser
import MouseClick
import WherePDF
import Gol

MouseClick = MouseClick.MouseClick()
GetPDF2Data = WherePDF.movePDF()
class ReadFile:
    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time
    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        log_data_Text = Gol.get_value("log_data_Text")
        LOG_LINE_NUM = Gol.get_value("LOG_LINE_NUM")
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            log_data_Text.insert("end", logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
            Gol.set_value("LOG_LINE_NUM", LOG_LINE_NUM)
        else:
            log_data_Text.delete(1.0,2.0)
            log_data_Text.insert("end", logmsg_in)

    # 通过完整路径获取数据
    def GetThesisData(self,path):
        f = open(path,encoding='utf-8')
        data = f.readlines()
        return data

    # 把数据集进行处理-》提取出名字
    def AnsisyThesis(self,data):
        url_list = []
        thesis_list = []
        for i in data:
            pattern = re.compile(r'.*http.*')
            url = u'' + i
            if(pattern.findall(url) == []):
                # 是否包括序号：
                num_pattern = re.compile(r'\[[0-9]+]')
                num = u'' + i
                if(num_pattern.findall(num)!=[]):
                    tmp_h = i.split('.')
                    for index, j in enumerate(tmp_h):
                        if index != 0:
                            thesis_pattern = re.compile(r'.*\[.*].*')
                            thesis = u'' + j
                            if(thesis_pattern.findall(thesis)!=[]):
                                tmp_b = j.split('//')
                                thesis_list.append(tmp_b[0])
                else:
                    tmp_h = i.split('.')
                    for index, j in enumerate(tmp_h):
                        thesis_pattern = re.compile(r'.*\[.*].*')
                        thesis = u'' + j
                        if(thesis_pattern.findall(thesis)!=[]):
                            tmp_b = j.split('//')
                            thesis_list.append(tmp_b[0])
            else:
                url_pattern = re.compile(r'http.*')
                url = u'' + i
                url_list.append(url_pattern.findall(url))
        return thesis_list,url_list

class Pdf_Deal:
    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        log_data_Text = Gol.get_value("log_data_Text")
        LOG_LINE_NUM = Gol.get_value("LOG_LINE_NUM")
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            log_data_Text.insert("end", logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
            Gol.set_value("LOG_LINE_NUM", LOG_LINE_NUM)
        else:
            log_data_Text.delete(1.0,2.0)
            log_data_Text.insert("end", logmsg_in)

    def proxies_spider(self,canshu):
        SetJson = Gol.get_value("SetJson")
        '''
        使用代理的爬虫
        :param canshu: 用字典包裹的参数
        canshu = {
            'url': 'url',
            'cookie': 'cookie',
            ……
        }
        :return:
        '''

        # 代理设置
        proxies = {
            'https': SetJson["proxies"],  # 查找到你的vpn在本机使用的https代理端口
            # 'http': 'http://74.207.240.85:4781',  # 查找到vpn在本机使用的http代理端口
        }

        # 请求的链接
        url = canshu['url']

        # 请求的参数
        data = {

        }

        # 请求的头部
        headers = {
            'user-agent': SetJson['cookie'],  # 全局变量
            'Cookie': SetJson['user_agent']  # 有需要则传入cookie
        }

        # request增加代理设置
        opener = request.build_opener(request.ProxyHandler(proxies))
        request.install_opener(opener)

        # get请求
        try:
            req_result = requests.get(url=url, params=data, headers=headers, proxies=proxies)
        except:
            self.write_log_to_Text("\n警告异常 (code100)：Max retries exceeded with url")
        # post请求
        # req_result = requests.post(url=url, data=data, headers=headers, proxies=proxies)

        # 如果是html页面：
        req_result = req_result.text

        html = BeautifulSoup(req_result, features="html.parser")

        # 如果是json数据：
        # req_result = req_result.json()

        return html

    # 获取网页
    def getHTML(self,url):
        SetJson = Gol.get_value("SetJson")
        global user_agent
        # 访问的浏览器信息
        user_agent = SetJson['user_agent']

        canshu = {
            'url': url,  # 请求的链接
            # 'cookie': 'AEC=AakniGO7W1A933pO4962IZpm2F1ng9ZWY9QV_m-S7Y5b89lpyIn_nHguN_0; 1P_JAR=2022-08-03-11; NID=511=XiJn5Yj8zX_QKJ5OGo2NhU0B8oXqFftF_eUE36W0s_wqHlmSSvqdL5y9H3vBoVb_DSHkTwQBA2-DIFZ5uhEjMPrfGbFU7zEQzD9IF_cMm2OfuSxeyj13bDhdFBSS9Rol3LUYVoh3HVE6og5byt9WxyUY95FrPcNKqVQCt8jtHTH5NgBv2gzCgFn1p6dQMC5E7x3VB6oajg; GSP=A=nsyI-w:CPTS=1659528933:LM=1659528933:S=q0J08u6h1byTTADu',  # 请求的cookie，如果不需要可以留空
            'cookie': SetJson['cookie'],  # 请求的cookie，如果不需要可以留空
        }

        req_result = self.proxies_spider(canshu)

        return req_result

    def GetThesisList(self,data,SetJson):
        thesis_list = []
        url_pre = SetJson['url']
        for i in data:
            url = url_pre+i
            html = self.getHTML(url)
            h3 = html.find_all('h3')
            lists = []
            for i in h3:
                a = i.find('a')
                if a!=None:
                    lists.append(a.get('href'))
            thesis_list.append(lists)
        return thesis_list
    # 获取pdf
    def GetThesisPDF(self,thesis_list,thesis_list_url,SetJson):
        for i in range(len(thesis_list)):
            if thesis_list_url[i]==[]:
                self.write_log_to_Text(thesis_list[i]+"文件寻找失败")
                print(thesis_list[i]+"文件寻找失败")
            else:
                # 打开连接，点击获取pdf，运行转移，发现新转移，认为找到pdf了
                # print(".........")
                # self.write_log_to_Text(".........")
                for index, j in enumerate(thesis_list_url[i]):
                    webbrowser.open_new(j)
                    # 等待页面打开
                    time.sleep(int(SetJson['wait_web']))
                    MouseClick.Click_once(SetJson)
                    # 等待pdf被下载
                    time.sleep(int(SetJson['wait_pdf']))
                    # 等待pdf验证
                    FindTrue,PDF_NAME = GetPDF2Data.GetPDF2Data(SetJson)

                    if FindTrue:
                        Now_Path = os.getcwd()
                        UserSetFileName = SetJson["log_name"]
                        # notfind_name
                        Dir_Name = Now_Path + "\\" + UserSetFileName
                        # 写入日志文件
                        f = open(Dir_Name, "a",encoding='utf-8')
                        # 写入配置名称
                        f.write("\n" + time.asctime() + "-----" + thesis_list[i] + "-------->"+PDF_NAME+",")
                        print(time.asctime() + "-----" + thesis_list[i] + "-------->"+PDF_NAME)
                        self.write_log_to_Text(time.asctime() + "-----" + thesis_list[i] + "-------->"+PDF_NAME)

                        break
                    else:
                        self.write_log_to_Text(thesis_list[i] + "文件寻找第"+str(index+1)+"次失败")
                        print(thesis_list[i] + "文件寻找第"+str(index+1)+"次失败")
                    if index == len(thesis_list_url[i])-1:
                        Now_Path = os.getcwd()
                        UserSetFileName = SetJson["notfind_name"]
                        Dir_Name = Now_Path + "\\" + UserSetFileName
                        print(thesis_list[i]+"查找失败")
                        # 写入日志文件
                        f = open(Dir_Name, "a", encoding='utf-8')
                        # 写入配置名称
                        self.write_log_to_Text(thesis_list[i] + "-------->查找失败,写入日志notfind.pdf")
                        f.write("\n" + thesis_list[i] + "-------->查找失败,")



