#include "huart1.h"
#include "usart.h"

#include "stm32f4xx_hal_uart.h"

#include "../driver/ringbuffer.h"

ring_buffer_t huart1_rx_ringbuffer;

ring_buffer_t huart1_tx_ringbuffer;//发送缓存


void huart1_init(void)
{
	ring_buffer_init(&huart1_rx_ringbuffer);
	ring_buffer_init(&huart1_tx_ringbuffer);

	__HAL_UART_CLEAR_FLAG(&huart1,UART_FLAG_TC);
}



void huart1_rx_calllback(uint8_t rx)
{
	ring_buffer_queue(&huart1_rx_ringbuffer,rx);

}


uint16_t huart1_rx(uint8_t *buffer, uint16_t size)
{

	if (buffer == NULL || size == 0){
		return 0;
	}


	return ring_buffer_dequeue_arr(&huart1_rx_ringbuffer,(char *)buffer,size);




}









//串口7 被设计成有TX接口
uint16_t huart1_tx(uint8_t *buffer,uint16_t size)
{
	//加入缓冲区
	ring_buffer_queue_arr(&huart1_tx_ringbuffer,(const char *)buffer,size);

	return 0;
}

//
void huart1_tx_polling(void)
{
	char temp;

	if (__HAL_UART_GET_FLAG(&huart1,UART_FLAG_TXE) == true){
		//发送寄存器空
		if (ring_buffer_dequeue(&huart1_tx_ringbuffer,&temp) > 0){
			//抽取到了数据

			USART1->DR = temp;
		}else{
			//没有数据,检查发送是否完成
			if (__HAL_UART_GET_FLAG(&huart1,UART_FLAG_TC) == true){
				//移位寄存器发送完成

			}else{
				//移位寄存器发送未完成
			}
		}
	}else{
		//发送寄存器非空
	}


}


//发送完成回调函数
void huart1_tx_complete_callback(void)
{


}



