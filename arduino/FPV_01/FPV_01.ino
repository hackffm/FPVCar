
int BIN_1 = 5;
int BIN_2 = 6;
int AIN_1 = 3;
int AIN_2 = 9;
int MAX_PWM_VOLTAGE = 40;

void setup() {
  Serial.begin(9600);
  
  pinMode(BIN_1, OUTPUT);
  pinMode(BIN_2, OUTPUT);
  pinMode(AIN_1, OUTPUT);
  pinMode(AIN_2, OUTPUT);
}

void loop() {
  receive_serial_cmd();
}

void receive_serial_cmd(void) {
  static uint8_t cmd[18];         // command buffer
  static uint8_t cmdcount = 0;    // position in the buffer of the received byte
  uint8_t c;                      // received byte
  while(Serial.available()) {
    c = Serial.read();
    if(c > ' ') cmd[cmdcount++] = c;
    if((c == 8) && (cmdcount > 0)) cmdcount--;                // deals with backspaces, if a person on the other side types 
    if((c == 0x0d) || (c == 0x0a) || (cmdcount > 16)) {       // end of command, gets interpreted now
      cmd[cmdcount] = 0;    // clear the last byte in cmd buffer
      if(cmdcount > 0) {    // prevent empty cmd buffer parsing
       switch(cmd[0]) {
        case 'l': 
          if((cmdcount > 2) && (cmdcount < 7)) {
            int temp = atoi((const char *)&cmd[1]);           
            Serial.print("l:");
            Serial.println(temp);  
  
            if(temp > 0) {
              if(temp > 255) temp = 255;
              digitalWrite(BIN_1, HIGH);
              digitalWrite(BIN_2, LOW);
              analogWrite(BIN_1, temp);                    
            } else {
              temp = -temp;
              if(temp > 255) temp = 255;
              digitalWrite(BIN_1, LOW);
              digitalWrite(BIN_2, HIGH);
              analogWrite(BIN_2, temp); 
            }
          }                    
          break; 
          case 'r':
           if((cmdcount > 2) && (cmdcount < 7)) {
            int temp = atoi((const char *)&cmd[1]);           
            Serial.print("r:");
            Serial.println(temp);
            
            if(temp > 0) {
              if(temp > 255) temp = 255;
              digitalWrite(AIN_1, HIGH);
              digitalWrite(AIN_2, LOW);
              analogWrite(AIN_1, temp);                    
            } else {
              temp = -temp;
              if(temp > 255) temp = 255;
              digitalWrite(AIN_1, LOW);
              digitalWrite(AIN_2, HIGH);
              analogWrite(AIN_2, temp); 
            }                        
          }  
          break; 
          case 'e':   // echo
          Serial.println("echo");
          break;
       }    
      }
      cmdcount = 0;
    } 
  }
}
