#coding=utf-8

import os
import re

def get_path_by_filename( rootpath,  filename ) :
    print("获取文件列表")

    lst = [] #返回列表

    for root, dirs , files in os.walk(rootpath) :
        for name in enumerate(files) :
            if (name[1] == filename) :
                print("---------- 找到文件 -----------")
                print(root + "/" +name[1])
                lst.append(root + "/" + name[1])


    return lst




def get_path_by_filename_regex( rootpath,  filename ) :
    print("获取文件列表")

    lst = [] #返回列表

    for root, dirs, files in os.walk(rootpath):
        for name in enumerate(files):
            if re.match(filename, name[1]):
                print("---------- 找到文件 -----------")
                print(root + "/" + name[1])
                lst.append(root + "/" + name[1])


    return lst




if __name__ == "__main__" :

    print("文件")

    lst = get_path_by_filename("../code", "usart.c")



    print(lst)

    lst = get_path_by_filename_regex("../code", r'.+\.uvprojx')

    print(lst)

