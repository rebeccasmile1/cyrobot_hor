#coding=utf-8
from xml.dom.minidom import parse
import xml.dom.minidom

from python import cylib_file


def patch_settings_add_include( new ):
    list = cylib_file.get_path_by_filename_regex("../code", r'.+\.uvprojx') #正则获取所有工程配置文件

    if len(list) == 1:
        print("发现工程配置文件，开始patch....")

        try:
            f = open(list[0])

            data = f.read()

            print(data)

            #解析xml

            # 使用minidom解析器打开 XML 文档
            DOMTree = xml.dom.minidom.parse(list[0])

            print("xmldom.parse:", type(DOMTree))

            object = DOMTree.documentElement
            print("document element:", type(object))

            # 获得子标签
            subElementObj = object.getElementsByTagName("IncludePath")
            print("getElementsByTagName:", type(subElementObj))

            print(subElementObj[1].firstChild.data)


            include = subElementObj[1].firstChild.data

            include_list = str(include).split(";")

            print(include_list)

            include_new = include + ";"+str(new)

            print(include_new)





        finally:
            if f:
                f.close()



    else:
        print("发现多个工程配置文件，无法 patch ， 下个版本修复")






if __name__ == "__main__":
    patch_settings_add_include("../cylib/")