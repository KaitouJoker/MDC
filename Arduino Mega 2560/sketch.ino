#include <SPI.h>  
#include <Pixy.h>

Pixy pixy;
String xywh;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial.print("Starting...\n");
  
  pixy.init();
}

void loop() { 
    static int i = 0;
    int j;
    uint16_t blocks;

    // grab blocks!
    blocks = pixy.getBlocks();
    if (blocks) {
        i++;
        if (i%1==0) {
            for (j=0; j<blocks; j++) {
                xywh = pixy.blocks[j].print();
                Serial.println(xywh);
            }
        }
    }
    delay(1);
}