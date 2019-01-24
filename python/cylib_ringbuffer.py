#coding=utf-8


import os



global ringbuffer_h_data




global ringbuffer_c_data




def generator_h_file( name ) :
    global ringbuffer_h_data
    global ringbuffer_c_data

    h_data = ringbuffer_h_data;

    h_data = str(h_data).replace("RINGBUFFER_H", str(name).upper()+"_RINGBUFFER_H")

    h_data = str(h_data).replace("RING_BUFFER_SIZE", str(name).upper() + "_RING_BUFFER_SIZE")

    h_data = str(h_data).replace("ring_buffer_size_t", str(name).lower() + "_ring_buffer_size_t")

    h_data = str(h_data).replace("RING_BUFFER_MASK", str(name).upper() + "_RING_BUFFER_MASK")

    h_data = str(h_data).replace("ring_buffer_t", str(name).lower() + "_ring_buffer_t")

    h_data = str(h_data).replace("ring_buffer_init", str(name).lower() + "_ring_buffer_init")

    h_data = str(h_data).replace("ring_buffer_queue", str(name).lower() + "_ring_buffer_queue")

    h_data = str(h_data).replace("ring_buffer_queue_arr", str(name).lower() + "_ring_buffer_queue_arr")

    h_data = str(h_data).replace("ring_buffer_dequeue", str(name).lower() + "_ring_buffer_dequeue")

    h_data = str(h_data).replace("ring_buffer_dequeue_arr", str(name).lower() + "_ring_buffer_dequeue_arr")

    h_data = str(h_data).replace("ring_buffer_peek", str(name).lower() + "_ring_buffer_peek")

    h_data = str(h_data).replace("ring_buffer_is_empty", str(name).lower() + "_ring_buffer_is_empty")

    h_data = str(h_data).replace("ring_buffer_is_full", str(name).lower() + "_ring_buffer_is_full")

    h_data = str(h_data).replace("ring_buffer_num_items", str(name).lower() + "_ring_buffer_num_items")



    # print(h_data)

    return h_data


def generator_c_file( name ) :
    global ringbuffer_h_data
    global ringbuffer_c_data

    c_data = ringbuffer_c_data;

    c_data = str(c_data).replace("RINGBUFFER_H", str(name).upper()+"_RINGBUFFER_H")

    c_data = str(c_data).replace("RING_BUFFER_SIZE", str(name).upper() + "_RING_BUFFER_SIZE")

    c_data = str(c_data).replace("ring_buffer_size_t", str(name).lower() + "_ring_buffer_size_t")

    c_data = str(c_data).replace("RING_BUFFER_MASK", str(name).upper() + "_RING_BUFFER_MASK")

    c_data = str(c_data).replace("ring_buffer_t", str(name).lower() + "_ring_buffer_t")

    c_data = str(c_data).replace("ring_buffer_init", str(name).lower() + "_ring_buffer_init")

    c_data = str(c_data).replace("ring_buffer_queue", str(name).lower() + "_ring_buffer_queue")

    c_data = str(c_data).replace("ring_buffer_queue_arr", str(name).lower() + "_ring_buffer_queue_arr")

    c_data = str(c_data).replace("ring_buffer_dequeue", str(name).lower() + "_ring_buffer_dequeue")

    c_data = str(c_data).replace("ring_buffer_dequeue_arr", str(name).lower() + "_ring_buffer_dequeue_arr")

    c_data = str(c_data).replace("ring_buffer_peek", str(name).lower() + "_ring_buffer_peek")

    c_data = str(c_data).replace("ring_buffer_is_empty", str(name).lower() + "_ring_buffer_is_empty")

    c_data = str(c_data).replace("ring_buffer_is_full", str(name).lower() + "_ring_buffer_is_full")

    c_data = str(c_data).replace("ring_buffer_num_items", str(name).lower() + "_ring_buffer_num_items")

    c_data = str(c_data).replace("ringbuffer.h", str(name).lower() + "_ringbuffer.h")

    # print(c_data)

    return c_data






#name = "huart1"
#genpath = "./generator/"
def generator(name , genpath) :
    global ringbuffer_h_data
    global ringbuffer_c_data

    try:
        h = open("cylib/buffer/ringbuffer/ringbuffer.h")
        ringbuffer_h_data = h.read()
    finally:
        if h:
            h.close()

    try:
        c = open("cylib/buffer/ringbuffer/ringbuffer.c")
        ringbuffer_c_data = c.read()
    finally:
        if c:
            c.close()


    # print("=================================")
    #
    # print(ringbuffer_h_data)
    # print("=================================")
    #
    # print(ringbuffer_c_data)

    generator_file_list = [] #生成的文件列表

    h = generator_h_file(name)

    c = generator_c_file(name)

    if os.path.exists(genpath) == False:
        os.mkdir(genpath)
    else:
        print("generator exists !")

    print("检查文件是否存在")

    if str(genpath).endswith("/") == False :
        genpath = genpath + "/"

    if os.path.exists(genpath+name+"_ringbuffer.c") == False:
        print("目标文件不存在")
        try:
            os.mknod(genpath+name+"_ringbuffer.c")
            f = open(genpath+name+"_ringbuffer.c", "w")
            f.write(c)
        finally:
            if f:
                f.close()
    else:
        print("目标文件存在")

    if os.path.exists(genpath+name+"_ringbuffer.h") == False:
        print("目标文件不存在")
        try:
            os.mknod(genpath+name+"_ringbuffer.h")
            f = open(genpath+name+"_ringbuffer.h", "w")
            f.write(c)
        finally:
            if f:
                f.close()
    else:
        print("目标文件存在")

    generator_file_list.append(name+"_ringbuffer.c")
    generator_file_list.append(name+"_ringbuffer.h")

    return generator_file_list


if __name__ == "__main__" :





    #print(ringbuffer_h_data)

    generator("huart3","./generator/")#生成






