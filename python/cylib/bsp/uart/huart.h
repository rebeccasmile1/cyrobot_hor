#ifndef __huart1_h
#define __huart1_h



#include <stdint.h>
#include <stdbool.h>




void huart1_init(void);
void huart1_rx_calllback(uint8_t rx);
uint16_t huart1_rx(uint8_t *buffer, uint16_t size);
uint16_t huart1_tx(uint8_t *buffer,uint16_t size);
extern void huart1_tx_polling(void);
extern void huart1_tx_complete_callback(void);




#endif


