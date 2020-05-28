extern "C" char *sbrk(int i);

// Trinket M0, RX von IRDA an D3, Rest an +3.3V

// LED Pad PA10 SERCOM2.2
#include <Arduino.h>   // required before wiring_private.h
#include "wiring_private.h" // pinPeripheral() function

//D20 PA31 sercom1.3 RX
//D19 PA30 sercom1.2 TX

#define LED_WHITE 0
#define LED_UV 1
#define LED_LASER 2


// Serial2 (sercom 1)
#define PIN_SERIAL2_RX  (20ul) // PA07
#define PAD_SERIAL2_RX  (SERCOM_RX_PAD_3)
#define PIN_SERIAL2_TX  (19ul) // PA06
#define PAD_SERIAL2_TX  (UART_TX_PAD_2)   

#include <Adafruit_DotStar.h>

#define MAX_ENTRIES 16
#define ENTER_TRIGGER_COUNT 3
#define EXIT_TIMEOUT_MS 100

struct tag_entry {
  uint16_t id;
  uint32_t timestamp;
  uint16_t count;
} tags[MAX_ENTRIES];

uint32_t old_color;
uint32_t new_color;

Uart Serial2( &sercom1, PIN_SERIAL2_RX, PIN_SERIAL2_TX, PAD_SERIAL2_RX, PAD_SERIAL2_TX ) ;
Adafruit_DotStar strip = Adafruit_DotStar(1, INTERNAL_DS_DATA, INTERNAL_DS_CLK, DOTSTAR_BGR);

#define IDEVENTBUFFERLEN 128
char IDEventBuffer[IDEVENTBUFFERLEN];

void SERCOM1_Handler()
{
    Serial2.IrqHandler();
}

int FreeRam () {
  char stack_dummy = 0;
  return &stack_dummy - sbrk(0);
}
 
void txEn() {
  pinPeripheral(4, PIO_SERCOM_ALT);
  delayMicroseconds(10);
}

void txDis() {
  Serial1.flush();
  pinMode(4, INPUT_PULLUP);
} 
 
void setup() {
  // put your setup code here, to run once:
  pinMode(LED_WHITE, OUTPUT);
  pinMode(LED_UV, OUTPUT);
  pinMode(LED_LASER, OUTPUT);
  
  pinMode(4, OUTPUT);
  pinMode(3, INPUT_PULLUP);
  
  Serial.begin(115200);
  Serial1.begin(38400);
  Serial2.begin(100000, SERIAL_8E1);
  
  // Assign pins 19 & 20 SERCOM functionality
  pinPeripheral(PIN_SERIAL2_RX, PIO_SERCOM_ALT ); 
  pinPeripheral(PIN_SERIAL2_TX, PIO_SERCOM_ALT );

  txDis();

  strip.begin();
  strip.setBrightness(255);
  delay(100);
  strip.setPixelColor(0, 255, 255, 255); strip.show(); 
  delay(500);
  //strip.setPixelColor(0, 1, 1, 1); strip.show(); 

  
  SERCOM1->USART.CTRLA.bit.ENABLE = 0;
  while(SERCOM1->USART.SYNCBUSY.reg) {}
  
  SERCOM1->USART.CTRLA.bit.DORD = 0;
  //SERCOM1->USART.CTRLA.bit.SAMPR = 0;
  SERCOM1->USART.RXPL.reg = 4;
  while(SERCOM1->USART.SYNCBUSY.reg) {}
  SERCOM1->USART.CTRLB.bit.ENC = 1;
  while(SERCOM1->USART.SYNCBUSY.reg) {}
  
  SERCOM1->USART.CTRLA.bit.ENABLE = 1;
  while(SERCOM1->USART.SYNCBUSY.reg) {}
  

  for(int i=0; i<MAX_ENTRIES; i++) tags[i].id = 0;
  IDEventBuffer[0] = 0;
  new_color = 0x000200ul;
  old_color = 0;
}

void AddIDEvent(const char *s) {
  if((strlen(IDEventBuffer) + strlen(s) + 1) < IDEVENTBUFFERLEN) {
    strcat(IDEventBuffer, s);
  }      
}

// check one entry at a time
void id_table_worker() {
  static int i = 0;
  if(tags[i].id != 0) {
    if((uint32_t)(millis() - tags[i].timestamp) >= (uint32_t)EXIT_TIMEOUT_MS) {
      // timed out
      if(tags[i].count == 0) {
        uint16_t id = tags[i].id;
        char s[20];
        sprintf(s, "x%d;", id);
        AddIDEvent(s);
        // EXITED
        Serial.print("Exit ID: ");
        Serial.println(id);    
        if(id == 18) new_color &= ~((uint32_t)255 << 16);
        if(id == 19) new_color &= ~((uint32_t)255 << 8);    
      }
      tags[i].id = 0;
    }
  }
  i++;
  if(i >= MAX_ENTRIES) i=0;
}

void id_found(uint16_t id) {
  // try to find id
  int i;
  int next_free = -1;
  for(i=0; i<MAX_ENTRIES; i++) {
    if(tags[i].id == id) break;
    if(tags[i].id == 0) next_free = i;
  }
  if(i >= MAX_ENTRIES) {
    // not in list yet
    if(next_free >= 0) {
      tags[next_free].id = id;
      tags[next_free].timestamp = millis();
      tags[next_free].count = 1;
    } else {
      Serial.println("List full.");
    }
    
  } else {
    // found in list at position i
    tags[i].timestamp = millis();
    if(tags[i].count != 0) {
      tags[i].count++;
      if(tags[i].count >= ENTER_TRIGGER_COUNT) {
        char s[20];
        sprintf(s, "t%d;", id);
        AddIDEvent(s);
        tags[i].count = 0;
        // ENTERED
        Serial.print("Enter ID: ");
        Serial.println(id);

        if(id == 18) new_color |= ((uint32_t)32 << 16);
        if(id == 19) new_color |= ((uint32_t)32 << 8);
      }
    }
  }
  
}

uint8_t crc8(uint8_t dat, uint8_t crc) {
  crc ^= dat;
  for(uint8_t p=0; p<8; p++) {
    crc = crc & 0x80 ? (crc << 1) ^ 0x07 : crc << 1;
  }
  return crc;
}

void try_receive() {
  static uint32_t ustamp = micros();
  static uint8_t rx[4];
  static int idx = 0;
  
  while(Serial2.available()) { 
    if((uint32_t)(micros() - ustamp) > (uint32_t)120) {
      idx = 0;
    } 
    ustamp = micros();
    rx[idx++] = Serial2.read();
    if(idx >= 4) {
      uint8_t crc = 0;
      crc = crc8(rx[0], crc);
      crc = crc8(rx[1], crc);
      crc = crc8(rx[2], crc);
      if(crc == rx[3]) {
        uint16_t code = (uint16_t)rx[0] | ((uint16_t)rx[1]) << 8;
        if((rx[1] == 0) && ((rx[2] == 0x4f) || (rx[2] == 0x48))) {
          if(code != 0) id_found(code);
          //Serial.println(code, HEX);
        } else {
          //if(code != 0) id_found(code);
          Serial.print(rx[2], HEX);
          Serial.print(" - ");
          Serial.println(code, HEX);
          // 08 04 11 1b 03 0c 1d 02 1e 15
          // 0b 06 10 1c 0d 16 17 09 0e 13
          // 01 0a 1a 18 05 07 0f 19 14 12
        }
      }
        
      idx = 0;
    }
  }
  
}

 
void serialParser() {
  static char cmd[64];
  static byte charCount = 0;

  while(Serial1.available()) {
    // if any char in serial buffer available then do the parsing
    char c;
    c = Serial1.read(); // read one char from serial buffer
    if((c==8) && (charCount>0)) charCount--; // backspace

    if(c>=32) { // char in num char range then add char to cmd array
      cmd[charCount] = c;
      charCount++;
    }

    if((c==0x0D) || (c==0x0A) || (charCount>60)) 
    {
      // if the char is NL(New Line 0x0A) 
      // or CR (carriage return 0x0D) 
      // or cmd array buffer limit reached
      // parse the cmd buffer

      cmd[charCount]=0; // clear the last char in cmd buffer
      
      if(charCount>=1) { // prevent empty cmd buffer parsing

        switch(cmd[0]) {
            
          case 'T':
            if(charCount>=2) {
              int r, speed0, b;
              uint32_t color;
              
              switch(cmd[1]) {
                case '?':
                    txEn();
                    Serial1.println("cRRGGBB = RGB-LED, r = event receive, wx = white LED, ux = UV LED on off, lx = Laser : x = 0..255"); 
                    txDis();
                    break;
                  
                case 'c':
                    r = sscanf(&cmd[2],"%lx",&color);
                    if(r==1) new_color = color;
                    break;
                
                case 'p':
                    AddIDEvent("e333;");
                    break;
                  
                case 'r':
                    txEn();
                    Serial1.println(IDEventBuffer); 
                    IDEventBuffer[0] = 0;
                    txDis();
                    break;
                    
                case 'w': // white led
                    r = sscanf(&cmd[2],"%i",&b);
                    if(r==1) {
                      analogWrite(LED_WHITE, b);  
                    }
                    break;
                    
                case 'u': // uv led
                    r = sscanf(&cmd[2],"%i",&b);
                    if(r==1) {
                      if(b > 0) {
                        digitalWrite(LED_UV, HIGH);  
                      } else {
                        digitalWrite(LED_UV, LOW); 
                      }
                    }
                    break;
                     
                case 'l': // laser
                    r = sscanf(&cmd[2],"%i",&b);
                    if(r==1) {
                      analogWrite(LED_LASER, b);  
                    }
                    break;
                    
                default:
                  
                  break;
              }
            }
            break; // case 'T'
  
          default:
            Serial1.println("hae?\a");
            break;

        }
      }
      charCount = 0;
      //Serial1.print(">");
    }
  }
} 
 
void loop() {
  static uint32_t tstamp = millis();
  static uint32_t ustamp = micros();

  if((uint32_t)(millis() - tstamp) > (uint32_t)100) {
    tstamp += 100;
    //Serial1.write("X");
    //Serial.write("X");
  }
  
  // put your main code here, to run repeatedly:
  // C8,0,F2,AF  
  // 48,0,F2,79  
  // CRC8/ROHC 0x8B als Result? Check 0xD0, Init 0xFF, Poly 0x07
  /* 
   * 1248.1248
   * 0001.0011 0100.1111 1111.0101
   * 0001.0010 0100.1111 1001.1110
   * 
   */
    if(Serial.available()) {
      Serial2.write(Serial.read());
    }
    if(Serial2.available()) {
      try_receive();

      /*
      if((uint32_t)(micros() - ustamp) > (uint32_t)120) {
        Serial.println(" ");
      } else {
        Serial.print(",");
      }

      Serial.print(Serial1.read(), HEX);
      ustamp = micros();
      */
    }
    id_table_worker();
    if(old_color != new_color) {
      strip.setPixelColor(0, new_color); 
      strip.show();
      old_color = new_color;
    }
    serialParser();
}
