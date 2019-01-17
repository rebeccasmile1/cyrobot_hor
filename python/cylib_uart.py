#coding=utf-8

from python import cylib_file
import re #正则表达式

code_dectionary = "../code"








def get_all_uart_list():

    usart_list = []#串口列表

    print("正在扫描串口配置文件列表....")

    usart_configure_file_lst = cylib_file.get_path_by_filename(code_dectionary, "usart.c") #获取cubemx的串口配置文件列表

    print("扫描到的文件列表如下：")
    print(usart_configure_file_lst)  #打印列表

    if (len(usart_configure_file_lst) == 0) :
        print("未找到任何串口配置文件 ， 无法进行识别.....")
        return;

    for path in enumerate(usart_configure_file_lst) :
        print("正在处理 ... " + str(path))


        try :
            f = open(path[1], "r")

            data = str(f.read())

            next = 1 ##继续做

            while(next > 0) :
                res = re.search("UART_HandleTypeDef huart[0-9];", data)
                if res == None:
                    next = -1
                    continue;

                res = res.span();

                print(res)

                print(data[res[0]:res[1]])

                string = str(data[res[0]:res[1]])

                string = string.replace("UART_HandleTypeDef ","")
                string = string.replace(";", "")


                usart_list.append(string) #加入列表

                data = data[res[1]:len(data)]


            ###############    到此已经找到了所有的串口

            print("找到的串口列表为 ： ")

            print(usart_list)

        finally:
            if f:
                f.close()

    print("开始生成循环缓冲区")



















if __name__ == "__main__" :


    print("cylib_uart patch")

    get_all_uart_list()
















