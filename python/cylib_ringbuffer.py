#coding=utf-8


import os



ringbuffer_h_data = '''


#include <inttypes.h>

/**
 * @file
 * Prototypes and structures for the ring buffer module.
 */

#ifndef RINGBUFFER_H
#define RINGBUFFER_H

/**
 * The size of a ring buffer.
 * Due to the design only <tt> RING_BUFFER_SIZE-1 </tt> items
 * can be contained in the buffer.
 * The buffer size must be a power of two.
*/
#define RING_BUFFER_SIZE 128

#if (RING_BUFFER_SIZE & (RING_BUFFER_SIZE - 1)) != 0
#error "RING_BUFFER_SIZE must be a power of two"
#endif

/**
 * The type which is used to hold the size
 * and the indicies of the buffer.
 * Must be able to fit \c RING_BUFFER_SIZE .
 */
typedef uint8_t ring_buffer_size_t;

/**
 * Used as a modulo operator
 * as <tt> a % b = (a & (b − 1)) </tt>
 * where \c a is a positive index in the buffer and
 * \c b is the (power of two) size of the buffer.
 */
#define RING_BUFFER_MASK (RING_BUFFER_SIZE-1)

/**
 * Simplifies the use of <tt>struct ring_buffer_t</tt>.
 */
typedef struct ring_buffer_t ring_buffer_t;

/**
 * Structure which holds a ring buffer.
 * The buffer contains a buffer array
 * as well as metadata for the ring buffer.
 */
struct ring_buffer_t {
  /** Buffer memory. */
  char buffer[RING_BUFFER_SIZE];
  /** Index of tail. */
  ring_buffer_size_t tail_index;
  /** Index of head. */
  ring_buffer_size_t head_index;
};

/**
 * Initializes the ring buffer pointed to by <em>buffer</em>.
 * This function can also be used to empty/reset the buffer.
 * @param buffer The ring buffer to initialize.
 */
void ring_buffer_init(ring_buffer_t *buffer);

/**
 * Adds a byte to a ring buffer.
 * @param buffer The buffer in which the data should be placed.
 * @param data The byte to place.
 */
void ring_buffer_queue(ring_buffer_t *buffer, char data);

/**
 * Adds an array of bytes to a ring buffer.
 * @param buffer The buffer in which the data should be placed.
 * @param data A pointer to the array of bytes to place in the queue.
 * @param size The size of the array.
 */
void ring_buffer_queue_arr(ring_buffer_t *buffer, const char *data, ring_buffer_size_t size);

/**
 * Returns the oldest byte in a ring buffer.
 * @param buffer The buffer from which the data should be returned.
 * @param data A pointer to the location at which the data should be placed.
 * @return 1 if data was returned; 0 otherwise.
 */
ring_buffer_size_t ring_buffer_dequeue(ring_buffer_t *buffer, char *data);

/**
 * Returns the <em>len</em> oldest bytes in a ring buffer.
 * @param buffer The buffer from which the data should be returned.
 * @param data A pointer to the array at which the data should be placed.
 * @param len The maximum number of bytes to return.
 * @return The number of bytes returned.
 */
ring_buffer_size_t ring_buffer_dequeue_arr(ring_buffer_t *buffer, char *data, ring_buffer_size_t len);
/**
 * Peeks a ring buffer, i.e. returns an element without removing it.
 * @param buffer The buffer from which the data should be returned.
 * @param data A pointer to the location at which the data should be placed.
 * @param index The index to peek.
 * @return 1 if data was returned; 0 otherwise.
 */
ring_buffer_size_t ring_buffer_peek(ring_buffer_t *buffer, char *data, ring_buffer_size_t index);


/**
 * Returns whether a ring buffer is empty.
 * @param buffer The buffer for which it should be returned whether it is empty.
 * @return 1 if empty; 0 otherwise.
 */
inline ring_buffer_size_t ring_buffer_is_empty(ring_buffer_t *buffer) {
  return (buffer->head_index == buffer->tail_index);
}

/**
 * Returns whether a ring buffer is full.
 * @param buffer The buffer for which it should be returned whether it is full.
 * @return 1 if full; 0 otherwise.
 */
inline ring_buffer_size_t ring_buffer_is_full(ring_buffer_t *buffer) {
  return ((buffer->head_index - buffer->tail_index) & RING_BUFFER_MASK) == RING_BUFFER_MASK;
}

/**
 * Returns the number of items in a ring buffer.
 * @param buffer The buffer for which the number of items should be returned.
 * @return The number of items in the ring buffer.
 */
inline ring_buffer_size_t ring_buffer_num_items(ring_buffer_t *buffer) {
  return ((buffer->head_index - buffer->tail_index) & RING_BUFFER_MASK);
}

#endif /* RINGBUFFER_H */


'''




ringbuffer_c_data = '''

#include "ringbuffer.h"

/**
 * @file
 * Implementation of ring buffer functions.
 */

void ring_buffer_init(ring_buffer_t *buffer) {
  buffer->tail_index = 0;
  buffer->head_index = 0;
}

void ring_buffer_queue(ring_buffer_t *buffer, char data) {
  /* Is buffer full? */
  if(ring_buffer_is_full(buffer)) {
    /* Is going to overwrite the oldest byte */
    /* Increase tail index */
    buffer->tail_index = ((buffer->tail_index + 1) & RING_BUFFER_MASK);
  }

  /* Place data in buffer */
  buffer->buffer[buffer->head_index] = data;
  buffer->head_index = ((buffer->head_index + 1) & RING_BUFFER_MASK);
}

void ring_buffer_queue_arr(ring_buffer_t *buffer, const char *data, ring_buffer_size_t size) {
  /* Add bytes; one by one */
  ring_buffer_size_t i;
  for(i = 0; i < size; i++) {
    ring_buffer_queue(buffer, data[i]);
  }
}

ring_buffer_size_t ring_buffer_dequeue(ring_buffer_t *buffer, char *data) {
  if(ring_buffer_is_empty(buffer)) {
    /* No items */
    return 0;
  }
  
  *data = buffer->buffer[buffer->tail_index];
  buffer->tail_index = ((buffer->tail_index + 1) & RING_BUFFER_MASK);
  return 1;
}

ring_buffer_size_t ring_buffer_dequeue_arr(ring_buffer_t *buffer, char *data, ring_buffer_size_t len) {
  if(ring_buffer_is_empty(buffer)) {
    /* No items */
    return 0;
  }

  char *data_ptr = data;
  ring_buffer_size_t cnt = 0;
  while((cnt < len) && ring_buffer_dequeue(buffer, data_ptr)) {
    cnt++;
    data_ptr++;
  }
  return cnt;
}

ring_buffer_size_t ring_buffer_peek(ring_buffer_t *buffer, char *data, ring_buffer_size_t index) {
  if(index >= ring_buffer_num_items(buffer)) {
    /* No items at index */
    return 0;
  }
  
  /* Add index to pointer */
  ring_buffer_size_t data_index = ((buffer->tail_index + index) & RING_BUFFER_MASK);
  *data = buffer->buffer[data_index];
  return 1;
}

extern inline ring_buffer_size_t ring_buffer_is_empty(ring_buffer_t *buffer);
extern inline ring_buffer_size_t ring_buffer_is_full(ring_buffer_t *buffer);
extern inline ring_buffer_size_t ring_buffer_num_items(ring_buffer_t *buffer);

'''




def generator_h_file( name ) :

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



    print(h_data)

    return h_data


def generator_c_file( name ) :

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

    print(c_data)

    return c_data






#name = "huart1"
#genpath = "./generator/"
def generator(name , genpath) :

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






